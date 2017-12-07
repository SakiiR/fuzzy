# -*- coding: utf-8 -*-

import asyncio
from .request import Request

class Fuzzy(object):

    """ Fuzzy main object used to asm the others """

    def __init__(self, url, wordlist, verb, threads, headers, data, verbose, proxies, timeout, report, hc, ht, st):

        """ Constructor, store the configuration variable to the current object """

        self._url = url
        self._wordlist = wordlist
        self._verb = verb
        self._threads = threads
        self._headers = headers
        self._data = data
        self._verbose = verbose
        self._proxies = proxies
        self._timeout = timeout
        self._report = report
        self._hc = hc
        self._ht = ht
        self._st = st

    async def check_availibity(self):

        """ Check if the given url is alive """
        import time
        time.sleep(1)
        request = Request(self._url, self._headers, self._proxies, self._verb)  # TODO: implement the Request class
        return False

    async def process(self):
        if not await self.check_availibity():
            print("Url is not available .. exiting")
            return False
        print("Url Available !")
        return True



    def loop(self):

        """ Launch the main fuzzy loop after the url availibity """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.process())
        except KeyboardInterrupt:
            print("Interrupted!")
            pass
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
        return True
