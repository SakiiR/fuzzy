# -*- coding: utf-8 -*-


class Matching(object):

    """ Is used to match the response to keep or to leave """

    """
        TODO: We have to parse expressions ... in a efficient manner
              (without permitting code injection since people use sudo pip install ...):


        like: "status==404 and 'word' in content"
              "(status!=404 or 'word' in content) and word_count != 113"
    """
    @classmethod
    def advanded_filter_show(cls, status, content, a_filters):
        return True

    @classmethod
    def advanded_filter_hide(cls, status, content, a_filters):
        return False

    @classmethod
    def is_matching(cls, status, content, hc=[], hw=None, sw=None, sc=[], a_filters_s=None, a_filters_h=None):

        """ This classmethod is used to determinate if the given response match the given filters


            :param status: The HTTP response status code
            :param content: The HTTP response raw content
            :param hc: A list of HTTP status code that will hide the matching responses
            :param ht: A string that will hide response if it is matched in the given response content
            :param st: A string that will show response if it is matched is the given response contet

            :returns: a boolean -> True if the response has to be hide, False if it does not
        """

        # if a_filters_s is not None:
        #     if cls.advanded_filter_show(status, content, a_filters_s):
        #         return True
        # if a_filters_h is not None:
        #     if not cls.advanded_filter_hide(status, content, a_filters_h):
        #         return False

        # Hide if ht is in response content
        if hw is not None:
            if hw in content:
                return False
        # Show if st is in response content
        if sw is not None:
            if sw in content:
                return True
        # Show if status code is in hc array
        if len(sc) > 0:
            if status in sc:
                return True
        # Hide if status code is in hc array
        if len(hc) > 0:
            if status in hc:
                return False
        return True

