# -*- coding: utf-8 -*-


class Matching(object):

    """ Is used to match the response to keep or to leave """

    @classmethod
    def is_matching(cls, status, content, hc=[], ht=None, st=None):

        """ This classmethod is used to determinate if the given response match the given filters


            :param status: The HTTP response status code
            :param content: The HTTP response raw content
            :param hc: A list of HTTP status code that will hide the matching responses
            :param ht: A string that will hide response if it is matched in the given response content
            :param st: A string that will show response if it is matched is the given response contet

            :returns: a boolean -> True if the response has to be hide, False if it does not
        """

        # Hide if ht is in response content
        if ht is not None:
            if ht in content:
                return False
        # Show if st is in response content
        if st is not None:
            if st in content:
                return True
        # Hide if status code is in hc array
        if len(hc) > 0:
            if status in hc:
                return False
        return True

