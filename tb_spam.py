# -*- coding: utf-8 -*-

"""
This tb_spam is plugin for reject trackback.
This plugin judge trackback spam when received trackback
don't include our blog url.
"""

__AUTHOR__ = 'shunuhs'
__VERSION__ = '0.2.20200620'
__LICENSE__ = 'BSD license'
__UPDATED_BY__ = 'Junji NAKANISHI'

import urllib.request
from urllib.error import URLError


def cb_trackback_reject(args):
    request = args['request']
    comment = args['comment']
    config = request.get_configuration()
    my_url = config['base_url']
    if 'link' in comment:
        try:
            with urllib.request.urlopen(comment['link']) as f:
                content = f.read()
                if content.find(my_url) == -1:
                    return True
                else:
                    return False
        except URLError:
            return True
    else:
        return False
