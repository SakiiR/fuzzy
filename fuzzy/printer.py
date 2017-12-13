# -*- coding: utf-8 -*-

from urllib.parse import urlparse
from colored import fg, attr
from pwn import log


class Printer(object):

    """ Used to print results """

    @classmethod
    def first(cls):

        """ Display the first array element """

        log.info("+----------------------------------+---------+------------------------+----------------+----------------+----------------+--------------------+")
        log.info("|              URL                 |  CODE   |          TIMING        |      SIZE      |      WORDS     |      LINES     |    WORD PRESENT    |")
        log.info("+----------------------------------+---------+------------------------+----------------+----------------+----------------+--------------------+")

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
    def one(cls, url, code, timing, size, color, words, lines, word_present):

        """ Display an entry in the table """
        timing += "ms"
        path = urlparse(url).path
        out = ("|{}|{}{}{}|{}|{}|{}|{}|{}|".format(
            ' ' + path[:33] + ((33 - len(path)) * " "),
            ' ' + fg(color) , code[:8] + ((8 - len(code)) * " ") , attr('reset'),
            ' ' + timing[:23] + ((23 - len(timing)) * " "),
            ' ' + size[:15] + ((15 - len(size)) * " "),
            ' ' + words[:15] + ((15 - len(words)) * " "),
            ' ' + lines[:15] + ((15 - len(lines)) * " "),
            ' ' + word_present[:19] + ((19 - len(word_present)) * " "),
        ))
        log.warning(out)

    @classmethod
    def end(cls):

        """ End the table """

        log.info("+----------------------------------+---------+------------------------+----------------+----------------+----------------+--------------------+")


