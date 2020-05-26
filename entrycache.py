# vim: tabstop=4 shiftwidth=4 expandtab
"""
entrycache.py
Caches entry timestamps of the original creation date

If you want to manually create the cachefile, place a file
called .entrycache containing
{}
in your datadir  directory. This file needs to be
writable by your webserver.

If you do not want to create this file, it will automatically
be created in your datadir.

Original Author: Joe Topjian <joe@terrarum.net>
"""

__author__ = 'Junji NAKANISHI <jun-g@daemonfreaks.com>'
__version__ = '0.1.20200526'
__url__ = 'https://github.com/daemonfreaks/pyblosxom-plugins'


from os import path, stat
import pprint


def cb_start(args):

    request = args["request"]
    config = request.getConfiguration()
    data = request.getData()

    if path.isfile(path.join(config['datadir'], '.entrycache')):
        with open(path.join(config['datadir'], '.entrycache')) as f:
            data['cache'] = eval(f.read())
            f.close()
    else:
        with open(path.join(config['datadir'], '.entrycache'), 'w') as f:
            f.write("{}")
            f.close()
            data['cache'] = {}

    data['cachefile'] = path.join(config['datadir'], '.entrycache')
    request.addData(data)


def cb_filestat(args):
    request = args["request"]
    data = request.getData()
    cache = data["cache"]
    config = request.getConfiguration()
    key = args['filename'].replace(config['datadir'], '')
    if key in cache and cache[key]:
        mtime = []
        for i in args['mtime']:
            mtime.append(i)
        mtime[8] = cache[key]
        args['mtime'] = tuple(mtime)
    else:
        cache[key] = stat(args['filename'])[8]
        with open(data['cachefile'], 'w') as f:
            pprint.pprint(cache, f)
            f.close()
    return args
