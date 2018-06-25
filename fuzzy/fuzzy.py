# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import time
import logging
from datetime import datetime
try:
    from pwn import log
except Exception as e:
    print("You should install python3-pwntools log module !")
    print("> apt-get update")
    print("> apt-get install python3 python3-dev python3-pip git")
    print("> pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git")
    exit()
from .request import Request
from .utils import replace_kv_dict
from .matching import Matching
from .printer import Printer


g_exceptions = []


def print_exceptions():

    """ Print exceptions list """

    global g_exceptions
    for e in g_exceptions:
        log.warn("Exception occured : {}".format(e))


def exception_handler(loop, context):

    """ Asyncio loop exception handler


        :param loop: The main asyncio loop.
        :param context: The exception context.
    """

    global g_exceptions
    if 'exception' in context:
        g_exceptions.append(context['exception'])
    else:
        g_exceptions.append(context)


class Fuzzy(object):

    """ Fuzzy main object used to asm the others """

    def __init__(self,
                 url,
                 url_file,
                 wordlist,
                 verb,
                 limit,
                 delay,
                 headers,
                 data,
                 verbose,
                 timeout,
                 report,
                 hc, sc, hw, sw,
                 filter_show,
                 filter_hide,
                 tag,
                 disable_progress):

        """ Constructor, store the configuration variable to the current object """

        self._url = url
        self._url_file = url_file
        self._wordlist = wordlist
        self._verb = verb
        self._limit = limit
        self._delay = delay
        self._headers = headers
        self._tag = tag
        self._data = data
        self._disable_progress = disable_progress
        self._verbose = verbose
        self._timeout = timeout
        self._report = report
        self._hc = hc
        self._sc = sc
        self._hw = hw
        self._sw = sw
        self._filter_show = filter_show
        self._filter_hide = filter_hide
        self._requests_did = 0
        self._requests_todo = 0


    def forge_request(self, word, url):

        """ Replace the fuzzing tag into the configuration variables

            :param word: The word to replace in the headers, data and url fields.
        """

        # replace Headers
        headers = {k: v for (k, v) in self._headers.items()}
        replace_kv_dict(headers, self._tag, word)
        # replace Data
        data = ""
        if len(self._data) > 0:
            data = self._data.replace(self._tag, word)
        # replace URL
        nurl = url.replace(self._tag, word)
        return Request(url=nurl, headers=headers, data=data, verb=self._verb, word=word, timeout=self._timeout)

    def status(self, spent, word, extra=""):

        """ Display the progress status to the console

            :param spent: The request execution time
            :param word: The word that has been used
            :param extra Extra text to show
        """

        self._requests_did += 1
        self._percent_done = (self._requests_did * 100) / self._requests_todo
        started_duration = datetime.now() - self._starttime
        self._p.status('{}/{} {}% {}req/s - {} - {}'.format(
            self._requests_did,
            self._requests_todo,
            int(self._percent_done),
            int(self._requests_did / (started_duration.seconds + 1)),
            word,
            extra
        ))

    async def stop(self):

        """ Stop the loop """

        while not self._queue.empty():
            await self._queue.pop()
        self._queue.task_done()
        self.loop.stop()

    async def handle_request_exceptions(self, request):

        """ Handle the given requests errors !

            :param request: The request to handle
        """

        data = None
        try:
            data = await request.process()
        except aiohttp.InvalidURL as e:
            log.warning("Invalid URL, exiting ..")
            await self.stop()
        except aiohttp.ClientConnectionError as e:
            self.status(0, request._word, "Request failed !")
            color = Printer.get_code_color("ERROR")
            Printer.one("'" + request._word + "'", "ERROR", "0", "0", color, "0", "0", "N/A")
        return data

    async def call_request(self, request):

        """ Process the given request and display the result

            :param request: The Request object containing all the information needed to send the HTTP request.
        """

        self._last_start = time.time()
        data = await self.handle_request_exceptions(request)
        if data is None:
            return
        spent = int((time.time() - self._last_start) * 1000)
        response = data['response']
        content = data['text']
        if not self._disable_progress:
            self.status(spent, request._word)
        if Matching.is_matching(response.status,
                                content,
                                hc=self._hc,
                                sc=self._sc,
                                hw=self._hw,
                                sw=self._sw,
                                a_filters_h=self._filter_hide,
                                a_filters_s=self._filter_show):
            color = Printer.get_code_color(response.status)
            Printer.one("'{}'".format(request._word if self._url_file is None else request._url),
                        str(response.status),
                        str(spent),
                        str(len(content)),
                        color,
                        str(len(content.split(' '))),
                        str(len(content.splitlines())),
                        str(request._word in content))
        if self._delay > 0:
            await asyncio.sleep(self._delay)
        self._queue.task_done()

    async def consumer(self):

        """ Consume an item in the queue, then send it to the request processer """

        while True:
            request = await self._queue.get()
            await self.call_request(request)

    async def _fill_multiple_url(self):
        words = self._wordlist.read().splitlines()
        for url in self._url_file.read().splitlines():
            await self._queue.put(self.forge_request("", url))
            for word in words:
                request = self.forge_request(word, url)
                await self._queue.put(request)
        self._requests_todo = self._queue.qsize()

    async def fill_queue(self):

        """ Fill the tasks queue """

        if self._url_file is not None:
            await self._fill_multiple_url()
            return
        await self._queue.put(self.forge_request("", self._url))
        for word in self._wordlist.read().splitlines():
            request = self.forge_request(word, self._url)
            await self._queue.put(request)
        self._requests_todo = self._queue.qsize()

    async def trigger_coros(self):

        """ Launch and gather the coroutines """

        coros = (self.consumer() for _ in range(self._limit))
        task = self.loop.create_task(asyncio.gather(*coros))
        await self._queue.join()

    async def process(self):

        """ Main task to process

            * Check given url availability
            * Fill test tasks queue
            * Launch the task
        """

        self._queue = asyncio.Queue()
        await self.fill_queue()
        log.info("Launching {} requests ..".format(self._requests_todo))
        if not self._disable_progress:
            self._p = log.progress('Status')
        Printer.first()
        self._starttime = datetime.now()
        await self.trigger_coros()
        self.loop.stop()

    def loop(self):

        """ Launch the main fuzzy loop """

        self.loop = asyncio.get_event_loop()
        # self.loop.set_debug(True)
        # self.loop.set_exception_handler(exception_handler)
        try:
            self.loop.run_until_complete(self.process())
        except KeyboardInterrupt as e:
            Printer.end()
            log.warning("Interrupted !")
            if self._verbose:
                print_exceptions()
            exit()
        Printer.end()
        log.warning("Ending !")
        if self._verbose:
            print_exceptions()
