# -*- coding: utf-8 -*-

import asyncio
import requests


class Request(object):

    """ The request class used to send HTTP request and storing the result """

    def __init__(self, url, headers={}, data={}, verb="GET", word=None, timeout=0):

        self._word = word
        self._url = url
        self._headers = headers
        self._data = data
        self._verb = verb
        self._timeout = timeout

    def process(self):
        verbs = {
            'GET': requests.get,
            'HEAD': requests.head,
            'POST': requests.post,
            'OPTIONS': requests.options
        }
        args = {
            'headers': self._headers
        }
        if len(self._data) > 0 and self._verb == 'POST':
            args['data'] = data
        response = verbs[self._verb](self._url, **args)
        return {'response': response, 'word': self._word}

