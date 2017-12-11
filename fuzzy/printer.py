# -*- coding: utf-8 -*-

from pwn import log

class Printer(object):

    """ Used to print results """

    @classmethod
    def first(cls):

        """ Display the first array element """

        log.info("+----------------------------------+---------+------------------------+----------------+")
        log.info("|              URL                 |  CODE   |          TIMING        |      SIZE      |")
        log.info("+----------------------------------+---------+------------------------+----------------+")

    @classmethod
    def one(cls, url, code, timing, size):

        """ Display an entry in the table """

        log.warning("|{}|{}|{}|{}".format(
            url[:34] + ((33 - len(url)) * " "),
            code[:9] + ((9 - len(code)) * " "),
            code[:24] + ((24 - len(timing)) * " "),
            code[:16] + ((16 - len(code)) * " "),
        ))



