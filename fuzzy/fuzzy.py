# -*- coding: utf-8 -*-

import asyncio
import time
import logging
from datetime import datetime
from pwn import log
from .request import Request
from .utils import replace_kv_dict
from .matching import Matching
from .printer import Printer


def exception_handler(loop, context):

    """ Asyncio loop exception handler """

    if 'exception' in context:
        log.warning("Exception occured: {}".format(context['exception'].args))


class Fuzzy(object):

    """ Fuzzy main object used to asm the others """

    def __init__(self, url, wordlist, verb, limit, headers, data, verbose, timeout, report, hc, ht, st, tag, disable_progress):

        """ Constructor, store the configuration variable to the current object """

        self._url = url
        self._wordlist = wordlist
        self._verb = verb
        self._limit = limit
        self._headers = headers
        self._tag = tag
        self._data = data
        self._disable_progress = disable_progress
        self._verbose = verbose
        self._timeout = timeout
        self._report = report
        self._hc = hc
        self._ht = ht
        self._st = st

    def forge_request(self, word):

        """ Replace the fuzzing tag into the configuration variables """

        # replace Headers
        new_headers = {k: v for (k, v) in self._headers.items()}
        replace_kv_dict(new_headers, self._tag, word)
        # replace Data
        new_data = {k: v for (k, v) in self._data.items()}
        replace_kv_dict(new_data, self._tag, word)
        # replace URL
        url = self._url.replace(self._tag, word)
        return Request(url=url, headers=new_headers, data=new_data, verb=self._verb, timeout=self._timeout)

    def response_content(self, response):

        """ Read all the content from the HTTP response """

        return response.content.decode('utf-8')


    async def call_request(self, request):

        """ Process the given request and display the result """

        start = time.time()
        started_duration = datetime.now() - self._starttime
        done_requests = self._total_requests - self._queue.qsize()
        percent_done = (100 - (self._queue.qsize() * 100 / self._total_requests))
        if not self._disable_progress:
            self._p.status('{}/{} {}% {}req/s - {}'.format(
                done_requests,
                self._total_requests,
                int(percent_done),
                int(done_requests / (started_duration.seconds + 1)),
                request._url,
            ))
        response = await request.process()
        spent = int((time.time() - start) * 1000)
        content = self.response_content(response)
        if Matching.is_matching(response.status_code, content, hc=self._hc, ht=self._ht, st=self._st):
            color = Printer.get_code_color(response.status_code)
            Printer.one(request._url, str(response.status_code), str(spent), str(len(content)), color)

    async def consumer(self):

        """ Consume an item in the queue, then send it to the request processer """

        while True:
            request = await self._queue.get()
            await self.call_request(request)
            self._queue.task_done()

    async def check_availibity(self):

        """ Check if the given url is alive """

        request = Request(self._url, self._headers, self._verb)
        try:
            response = await request.process()
        except Exception as e:
            print(e)
            response = None
        return response is not None

    async def fill_queue(self):

        """ Fill the tasks queue """

        for word in self._wordlist.read().splitlines():
            request = self.forge_request(word)
            await self._queue.put(request)

    async def process(self):

        """ Main task to process

            * Check given url availability
            * Fill test tasks queue
            * Launch the task
        """

        self._queue = asyncio.Queue()
        if not await self.check_availibity():
            log.warning("Url ({}) is not available .. exiting".format(self._url))
            return False
        log.success("Url Available ! ({})".format(self._url))
        log.info("Filling tasks queue !")
        await self.fill_queue()
        log.success("Tasks queue ready !")
        # TODO: Launch the tasks
        self._total_requests = self._queue.qsize()
        log.info("Launching {} requests ..".format(self._total_requests))
        if not self._disable_progress:
            self._p = log.progress('Status')
        Printer.first()
        self._starttime  = datetime.now()
        coros = (self.consumer() for _ in range(self._limit))
        task = self.loop.create_task(asyncio.gather(*coros))
        await self._queue.join()
        self.loop.stop()
        return True

    def loop(self):

        """ Launch the main fuzzy loop """

        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(exception_handler)
        self.loop.create_task(self.process())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        Printer.end()
        log.warning("Ending !")
