# -*- coding: utf-8 -*-


def replace_kv_dict(d, tag, word):

    """ Replace tag by word for each key and value of dict"""

    for k, v in d.items():
        new_k = k.replace(tag, word)
        new_v = v.replace(tag, word)
        d[new_k] = new_v
        if new_k != k:
            del d[k]
    return d

