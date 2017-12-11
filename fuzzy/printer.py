# -*- coding: utf-8 -*-

from colored import fg, attr
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
    def get_code_color(cls, code):

        """ Retrieve the HTTP status code color """

        color = 255
        if code in range(200, 299):
            color = 77
        elif code in range(300, 399):
            color = 169
        elif code in range(400, 499):
            color = 215
        elif code in range(500, 599):
            color = 9
        return color

    @classmethod
    def one(cls, url, code, timing, size, color):

        """ Display an entry in the table """

        log.warning("|{}|{}{}{}|{}|{}|".format(
            url[:34] + ((34 - len(url)) * " "),
            fg(color) , code[:9] + ((9 - len(code)) * " ") , attr('reset'),
            timing[:24] + ((24 - len(timing)) * " "),
            size[:16] + ((16 - len(size)) * " "),
        ))

    @classmethod
    def end(cls):

        """ End the table """

        log.info("+----------------------------------+---------+------------------------+----------------+")


