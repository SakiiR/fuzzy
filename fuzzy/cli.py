# -*- coding: utf-8 -*-

import argparse
import random
import pprint
from colored import fg, attr
from pwn import log
from .fuzzy import Fuzzy
from .logging import configure_logging


class HeadersAction(argparse.Action):

    """ Used to parse headers values from command line """

    def __call__(self, parser, namespace, values, option_string=None):
        headers = {}
        for value in values:
            data = value.split(":")
            if len(data) == 2:
                headers[data[0]] = data[1]
        setattr(namespace, self.dest, headers)


class DataAction(argparse.Action):

    """ Used to parse data values from command line """

    def __call__(self, parser, namespace, value, option_string=None):
        final_datas = {}
        data = value.split("&")
        for d in data:
            _ = d.split("=")
            if len(_) == 2:
                final_datas[_[0]] = _[1]
        setattr(namespace, self.dest, final_datas)


class IntListAction(argparse.Action):

    """ Used to parse comma separated list from command line """

    def __call__(self, parser, namespace, value, option_string=None):
        codes = []
        for code in value.split(","):
            try:
                codes.append(int(code))
            except ValueError:
                pass
        setattr(namespace, self.dest, codes)


class FuzzyCLI(object):


    """ Class use to handle fuzzy CLI """

    @classmethod
    def display_header(cls):

        """ Display the ascii header """

        draw = """
        {}   ______   __  __     ______     ______     __  __
        {}  /\\  ___\\ /\\ \\/\\ \\   /\\___  \\   /\\___  \\   /\\ \\_\\ \\
        {}  \\ \\  __\\ \\ \\ \\_\\ \\  \\/_/  /__  \\/_/  /__  \\ \\____ \\
        {}   \\ \\_\\    \\ \\_____\\   /\\_____\\   /\\_____\\  \\/\\_____\\
        {}    \\/_/     \\/_____/   \\/_____/   \\/_____/   \\/_____/
        {}
        {}
        {}
        {}  An other web fuzzer (  https://sakiir.ovh  )
        {}  - SakiiR
        {}
        {} /!\\ Use the #FUZZ# tag in your headers/datas/url to fuzz /!\\
        {}
        {}"""
        lines = len(draw.splitlines())
        mini = 0
        maxi = 255 - (lines + 1)
        rand_min = random.randint(mini, maxi)
        formater = [fg(color) for color in range(rand_min, rand_min + (lines - 2))] + [attr('reset')]
        draw = draw.format(*formater)
        print(draw)


    @classmethod
    def parse_args(cls, argv):

        """ Fuzzy Argument parser  """

        cls.display_header()
        parser = argparse.ArgumentParser(description="Python Web Fuzzer by SakiiR")
        parser.add_argument("--url", "-u", help="URL to fuzz", type=str, required=True)
        parser.add_argument("--wordlist", "-w", help="Wordlist to use for the fuzzing", type=argparse.FileType('r'), required=True)
        parser.add_argument("--verb", "-m", help="HTTP verb to be used (default GET)", choices=["GET", "HEAD", "POST", "OPTIONS", "PUT"], default="GET", type=str)
        parser.add_argument("--tag", "-t", help="Fuzzing tag to use (default #FUZZ#)", default="#FUZZ#", type=str)
        parser.add_argument("--limit", "-l", help="Number of tasks to be used (default 1)", default=1, type=int)
        parser.add_argument("--delay", "-s", help="Delay time after each requests (set --limit to 1)", default=0.0, type=float)
        parser.add_argument("--headers", "-e", help="Additional HTTP headers, eg: --headers \"foo: bar\" \"Content-Type: application/json\" (default none)", default={}, type=str, nargs="*", action=HeadersAction)
        parser.add_argument("--data", "-d", type=str, default={}, help="Data to send to the website via POST requests, eg: --data \"foo=bar&password=#FUZZ#\" (default none)", action=DataAction)
        parser.add_argument("--verbose", "-v", type=bool, help="Verbose mode - Display more information (default false)", const=True, nargs="?", default=False)
        parser.add_argument("--timeout", "-o", type=int, default=3000, help="Max timeout duration in ms (default 3000ms)")
        parser.add_argument("--report", "-r", type=argparse.FileType('w'), help="Report file to write in (default none)")
        parser.add_argument("--disable-progress", "-p", type=bool, help="Disable progress logging ( pwntools )", const=True, nargs="?", default=False)

        # Filters
        parser.add_argument("--hc", type=str, default=[], action=IntListAction, help="Hide given status code responses eg: --hc \"404, 400\" (default none)")
        parser.add_argument("--sc", type=str, default=[], action=IntListAction, help="Show given status code responses eg: --sc \"404, 400\" (default none)")
        parser.add_argument("--ht", type=str, help="Hide responses that match given str (default none)")
        parser.add_argument("--st", type=str, help="Show responses that match given str (default none)")
        return parser.parse_args(argv)

    @classmethod
    def main(cls, argv):

        """ Fuzzy main process """

        args = cls.parse_args(argv[1:])
        if args.verbose:
            log.info("[~] Configuration : ")
            pprint.pprint(vars(args))
        if args.delay > 0:
            args.limit = 1
        fuzzy = Fuzzy(**vars(args))
        configure_logging(verbose=args.verbose, report=args.report)
        fuzzy.loop()

