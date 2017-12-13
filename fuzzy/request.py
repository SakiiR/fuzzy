# -*- coding: utf-8 -*-

import asyncio
import aiohttp


class Request(object):

    """ The request class used to send HTTP request and storing the result """

    def __init__(self, url, headers={}, data={}, verb="GET", word=None, timeout=0):

        self._word = word
        self._url = url
        self._headers = headers
        self._data = data
        self._verb = verb
        self._timeout = timeout

    async def process(self):
        async with aiohttp.ClientSession(headers=self._headers, conn_timeout=self._timeout) as session:
            verbs = {
                'GET': session.get,
                'HEAD': session.head,
                'POST': session.post,
                'OPTIONS': session.options
            }
            args = {}
            if len(self._data) > 0 and self._verb == 'POST':
                args['data'] = data
            return await verbs[self._verb](self._url, **args)

