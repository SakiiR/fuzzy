#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import argparse
import random
from colored import fg, attr

ASCII = """
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


LINES = len(ASCII.splitlines())
MIN = 0
MAX = 255 - (LINES + 1)
RAND_MIN = random.randint(MIN, MAX)
FORMATER = [fg(color) for color in range(RAND_MIN, RAND_MIN + (LINES - 2))] + [attr('reset')]
ASCII = ASCII.format(*FORMATER)


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


def main(argv):

    """ Main process """
    print(ASCII)
    parser = argparse.ArgumentParser(description="Python Web Fuzzer by SakiiR")
    parser.add_argument("--url", "-u", help="URL to fuzz", type=str, required=True)
    parser.add_argument("--wordlist", "-w", help="Wordlist to use for the fuzzing", type=argparse.FileType('r'), required=True)
    parser.add_argument("--verb", "-m", help="HTTP verb to be used (default GET)", choices=["GET", "HEAD", "TRACE", "OPTION"], default="GET", type=str)
    parser.add_argument("--threads", "-t", help="Number of threads to be used (default 1)", default=1, type=int)
    parser.add_argument("--headers", "-he", help="Additional HTTP headers, eg: --headers \"foo: bar\" \"Content-Type: application/json\" (default none)", default={}, type=str, nargs="*", action=HeadersAction)
    parser.add_argument("--data", "-d", type=str, default={}, help="Data to send to the website via POST requests, eg: --data \"foo=bar&password=#FUZZ#\" (default none)", action=DataAction)
    parser.add_argument("--verbose", "-v", type=bool, help="Verbose mode - Display more information (default false)", const=True, nargs="?", default=False)
    parser.add_argument("--proxies", "-p", type=str, default=[], help="Simple http proxies to use (default none)")
    parser.add_argument("--timeout", "-ti", type=int, default=3000, help="Max timeout duration in ms (default 3000ms)")
    parser.add_argument("--report", "-r", type=argparse.FileType('w'), help="Report file to write in (default none)")

    # Filters
    parser.add_argument("--hc", type=str, default=[], action=IntListAction, help="Hide given status code responses eg: --hc \"404, 400\" (default none)")
    parser.add_argument("--ht", type=str, help="Hide responses that match given str (default none)")
    parser.add_argument("--st", type=str, help="Show responses that match given str (default none)")
    args = parser.parse_args(argv)
    print(args)


if __name__ == "__main__":
    main(sys.argv[1:])
