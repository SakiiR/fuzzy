# -*- coding: utf-8 -*-

import asyncio
import time
import logging
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pwn import log
from .request import Request
from .utils import replace_kv_dict
from .matching import Matching
from .printer import Printer


def exception_handler(loop, context):

    """ Asyncio loop exception handler """

    if 'exception' in context:
        log.warning("Exception occured: {}".format(context['exception']))


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
        self._max_worker = 4
        self._requests_did = 0
        self._requests_todo = 0

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

        self._last_start = time.time()
        def called_request(future):

            """ Callback for the request response """

            self._requests_did += 1
            response = future.result()
            self._percent_done = (self._requests_did * 100) / self._requests_todo
            started_duration = datetime.now() - self._starttime
            if not self._disable_progress:
                self._p.status('{}/{} {}% {}req/s - {}'.format(
                    self._requests_did,
                    self._requests_todo,
                    int(self._percent_done),
                    int(self._requests_did / (started_duration.seconds + 1)),
                    request._url,
                ))
            spent = int((time.time() - self._last_start) * 1000)
            content = self.response_content(response)
            if Matching.is_matching(response.status_code, content, hc=self._hc, ht=self._ht, st=self._st):
                color = Printer.get_code_color(response.status_code)
                Printer.one(request._url, str(response.status_code), str(spent), str(len(content)), color)
        f = self.executor.submit(request.process)
        f.add_done_callback(called_request)

    async def consumer(self):

        """ Consume an item in the queue, then send it to the request processer """

        while True:
            request = await self._queue.get()
            self._queue.task_done()
            await self.call_request(request)

    async def fill_queue(self):

        """ Fill the tasks queue """

        await self._queue.put(self.forge_request(""))
        for word in self._wordlist.read().splitlines():
            request = self.forge_request(word)
            await self._queue.put(request)
        self._requests_todo = self._queue.qsize()

    async def process(self):

        """ Main task to process

            * Check given url availability
            * Fill test tasks queue
            * Launch the task
        """

        self._queue = asyncio.Queue()
        log.success("Url Available ! ({})".format(self._url))
        log.info("Filling tasks queue !")
        await self.fill_queue()
        log.success("Tasks queue ready !")
        # TODO: Launch the tasks
        log.info("Launching {} requests ..".format(self._requests_todo))
        if not self._disable_progress:
            self._p = log.progress('Status')
        Printer.first()
        self._starttime  = datetime.now()
        coros = (self.consumer() for _ in range(self._max_worker))
        task = self.loop.create_task(asyncio.gather(*coros))
        await self._queue.join()
        self.executor.shutdown()
        Printer.end()
        log.warning("Ending !")
        time.sleep(1)
        self.loop.stop()
        return True

    def loop(self):

        """ Launch the main fuzzy loop """

        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=self._limit)
        self.loop.set_exception_handler(exception_handler)
        self.loop.create_task(self.process())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
