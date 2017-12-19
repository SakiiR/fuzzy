# -*- coding: utf-8 -*-

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


class Fuzzy(object):

    """ Fuzzy main object used to asm the others """

    def __init__(self,
                 url,
                 wordlist,
                 verb,
                 limit,
                 delay,
                 headers,
                 data,
                 verbose,
                 timeout,
                 report,
                 hc, sc, ht, st,
                 tag,
                 disable_progress):

        """ Constructor, store the configuration variable to the current object """

        self._url = url
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
        self._ht = ht
        self._st = st
        self._requests_did = 0
        self._requests_todo = 0

    def exception_handler(self, loop, context):

        """ Asyncio loop exception handler


            :param loop: The main asyncio loop.
            :param context: The exception context.
        """

        if self._verbose:
            if 'exception' in context:
                log.warning("Exception occured: {}".format(context['exception']))
            else:
                log.warning("Exception occures: {}".format(context))

    def forge_request(self, word):

        """ Replace the fuzzing tag into the configuration variables

            :param word: The word to replace in the headers, data and url fields.
        """

        # replace Headers
        new_headers = {k: v for (k, v) in self._headers.items()}
        replace_kv_dict(new_headers, self._tag, word)
        # replace Data
        new_data = {k: v for (k, v) in self._data.items()}
        replace_kv_dict(new_data, self._tag, word)
        # replace URL
        url = self._url.replace(self._tag, word)
        return Request(url=url, headers=new_headers, data=new_data, verb=self._verb, word=word, timeout=self._timeout)

    def status(self, spent, word):

        """ Display the progress status to the console

            :param spent: The request execution time
            :param word: The word that has been used
        """

        self._requests_did += 1
        self._percent_done = (self._requests_did * 100) / self._requests_todo
        started_duration = datetime.now() - self._starttime
        self._p.status('{}/{} {}% {}req/s - {}'.format(
            self._requests_did,
            self._requests_todo,
            int(self._percent_done),
            int(self._requests_did / (started_duration.seconds + 1)),
            word,
        ))

    async def call_request(self, request):

        """ Process the given request and display the result

            :param request: The Request object containing all the information needed to send the HTTP request.
        """

        self._last_start = time.time()
        data = await request.process()
        spent = int((time.time() - self._last_start) * 1000)
        response = data['response']
        content = data['text']
        if not self._disable_progress:
            self.status(spent, request._word)
        if Matching.is_matching(response.status, content, hc=self._hc, sc=self._sc, ht=self._ht, st=self._st):
            color = Printer.get_code_color(response.status)
            Printer.one("'" + request._word + "'", str(response.status), str(spent), str(len(content)), color, str(len(content.split(' '))), str(len(content.splitlines())), str(request._word in content))
        if self._delay > 0:
            await asyncio.sleep(self._delay)
        self._queue.task_done()

    async def consumer(self):

        """ Consume an item in the queue, then send it to the request processer """

        while True:
            request = await self._queue.get()
            await self.call_request(request)

    async def fill_queue(self):

        """ Fill the tasks queue """

        await self._queue.put(self.forge_request(""))
        for word in self._wordlist.read().splitlines():
            request = self.forge_request(word)
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

    def loop(self):

        """ Launch the main fuzzy loop """

        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(self.exception_handler)
        try:
            self.loop.run_until_complete(self.process())
        except KeyboardInterrupt:
            pass
        Printer.end()
        log.warning("Ending !")
