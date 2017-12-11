# -*- coding: utf-8 -*-

import logging


def configure_logging(verbose=False, report=None):

    """ Configure the logging module """

    if report is not None:
        loglevel = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(filename=report.name, format='%(asctime)s - %(message)s', level=loglevel)
        logging.info("URL,code,size,timing")


