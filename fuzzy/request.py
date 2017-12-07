# -*- coding: utf-8 -*-


class Request(object):

    """ The request class used to send HTTP request and storing the result """

    def __init__(self, url, headers={}, proxies=(), data={}, verb="GET"):

        self._url = url
        self._headers = headers
        self._proxies = proxies
        self._data = data
        self._verb = verb
