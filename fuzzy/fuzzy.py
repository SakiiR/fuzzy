# -*- coding: utf-8 -*-

from .request import Request


class Fuzzy(object):

    """ Fuzzy main object used to asm the others """

    def __init__(self, url, verb, threads, headers, data, verbose, proxies, timeout, report, hc, ht, st):

        """ Constructor, store the configuration variable to the current object """

        self._url = url
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

    def check_availibity(self):

        """ Check if the given url is alive """

        request = Request()  # TODO: implement the Request class
        return True

    def loop(self):

        """ Launch the main fuzzy loop after the url availibity """

        if not self.check_availibity():
            return False
        return True
