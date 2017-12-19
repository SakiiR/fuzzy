# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import async_timeout


class Request(object):

    """ The request class used to send HTTP request and storing the result """

    def __init__(self, url, headers={}, data="", verb="GET", word=None, timeout=0):

        self._word = word
        self._url = url
        self._headers = headers
        self._data = data
        self._verb = verb
        self._timeout = timeout

    async def process(self):

        """ Process the HTTP request  """

        async with aiohttp.ClientSession(headers=self._headers, conn_timeout=self._timeout) as session:
            verbs = {
                'GET': session.get,
                'HEAD': session.head,
                'POST': session.post,
                'OPTIONS': session.options,
                'PUT': session.put,
            }
            args = {}
            if len(self._data) > 0:
                args['data'] = self._data
                if self._verb not in ['POST', 'PUT']:
                    self._verb = 'POST'
            with async_timeout.timeout(10):
                async with verbs[self._verb](self._url, **args) as response:
                    return {
                        'response': response,
                        'text': await response.text()
                    }
            return "test"

