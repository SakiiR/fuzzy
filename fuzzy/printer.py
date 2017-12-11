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

        log.warning("|%s|%s|%s|%s|" % (
            url[:34] + ((34 - len(url)) * " "),
            code[:9] + ((9 - len(code)) * " "),
            timing[:24] + ((24 - len(timing)) * " "),
            size[:16] + ((16 - len(size)) * " "),
        ))

    @classmethod
    def end(cls):

        """ End the table """

        log.info("+----------------------------------+---------+------------------------+----------------+")


