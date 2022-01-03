# coding: utf-8
"""
entrymtime.py

This plugin provides to overwrite entry's mtime using metadata.
"""

__author__ = 'Junji NAKANISHI <jun-g@daemonfreaks.com>'
__version__ = '0.1.20220103'
__url__ = 'https://github.com/daemonfreaks/pyblosxom-plugins'

import os
import re
import time

try:
    from dateutil import parser
    _dateutil_is_installed = True
except ModuleNotFoundError:
    _dateutil_is_installed = False

_regexp = re.compile(r'\n#entrymtime\s+(.*)\n')


def verify_installation(request):
    return _dateutil_is_installed

def cb_filestat(args):
    request = args['request']
    config = request.get_configuration()
    filename = args['filename']
    fullname = os.path.join(config['datadir'], filename)
    with open(fullname, 'r') as f:
        contents = f.read()
        m = _regexp.search(contents)
        if m:
            try:
                mtime = []
                for i in args['mtime']:
                    mtime.append(i)
                mtime[8] = time.mktime(parser.parse(m.group(1)).timetuple())
                args['mtime'] = tuple(mtime)
            except:
                pass
    return args
