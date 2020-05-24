# coding: utf-8
"""
sitemap.py

This plugin generates a sitemaps.org compliant sitemap.xml when accessed
to `$base_url/sitemap.xml`.
This format is supported by Google, Yahoo, MSN.
See also http://www.sitemaps.org/
"""

__author__ = 'Junji NAKANISHI <jun-g@daemonfreaks.com>'
__version__ = 'version 0.1.20200524'
__url__ = 'https://github.com/daemonfreaks/pyblosxom-plugins'
__description__ = 'This is a PyBlosxom plugin that generates sitemap xml.'

import os.path
from Pyblosxom import tools, entries

TEMPLATE_BASE = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>"""

TEMPLATE_URL = """<url>
<loc>%s</loc>
<lastmod>%s</lastmod>
</url>"""


def cb_handle(args):
    request = args['request']
    data = request.getData()
    pyhttp = request.getHttp()
    config = request.getConfiguration()
    url = config.get('sitemap_url', '/sitemap.xml')
    if pyhttp['PATH_INFO'] != url:
        return 0
    response = request.getResponse()
    response.addHeader('Content-type', 'application/xml')
    urls = []
    for fname in tools.Walk(request, config['datadir']):
        entry = entries.fileentry.FileEntry(request, fname, config['datadir'])
        url = '%s.html' % (os.path.join(config['base_url'],
                                        entry.get('absolute_path'),
                                        entry.get('fn')))
        urls.append(TEMPLATE_URL % (url, entry.get('w3cdate')))
    urls.reverse()
    sitemap = TEMPLATE_BASE % ('\n'.join(urls))
    response.write(sitemap)
    return 1
