# -*- coding: utf-8 -*-

"""
This tb_spam is plugin for reject trackback.
This plugin judge trackback spam when received trackback
don't include our blog url.
"""

__AUTHOR__  = 'shunuhs'
__DATE__    = '2006/12/11 01:58 JST'
__VERSION__ = '0.1'
__LICENSE__ = 'BSD license'

def cb_trackback_reject(args):
    request = args['request']
    comment = args['comment']
    import urllib
    config = request.getConfiguration()
    my_url = config['base_url']
    if comment.has_key('link'):
        f = urllib.urlopen(comment['link'])
        content = f.read()
        f.close()
        if content.find(my_url) == -1:
            return True
        else:
            return False
    else:
        return False

