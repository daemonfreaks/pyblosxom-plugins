# coding: utf-8
"""
This plugin is the Open Graph protocol markup to your Pyblosxom blog.
To use, add the ``$ogp_tag`` variable to your head templates in the
<head> area.

Copyright 2011-2013 Junji NAKANISHI
"""

__author__ = 'Junji NAKANISHI'
__email__ = 'jun-g at daemonfreaks.com'
__version__ = '0.0.2'
__url__ = 'http://www.daemonfreaks.com/'
__description__ = 'The Open Graph protocol plugin'
__license__ = 'MIT'

_IMAGE_URL = 'http://pyblosxom.github.io/images/pb_pyblosxom.gif'
_TAG_TEMPLATE = '<meta property="%s" content="%s" />'

import re
import urlparse
from Pyblosxom import tools

_DESC_REGEXP = re.compile(r'<.*?>')
_IMG_REGEXP = re.compile(r'<img.*src=(["\'])?([^ "\']*)[^>]*>')


def verify_installation(request):

    return 1


def cb_prepare(args):

    request = args['request']
    config = request.get_configuration()
    data = request.get_data()
    entries = data['entry_list']
    elems = {}

    if config.get('ogp_fb_app_id'):
        elems['fb:app_id'] = config.get('ogp_fb_app_id')
    if config.get('ogp_fb_admins'):
        elems['fb:admins'] = config.get('ogp_fb_admins')

    image = None

    if len(entries) == 1:
        entry = entries[0]
        elems['og:type'] = 'article'
        elems['og:title'] = tools.escape_text(entry['title'].strip())
        elems['og:url'] = "%s/%s.html" % (config['base_url'],
                                          entry['file_path'])
        if len(entries) == 1 and config.get('ogp_fb_author_url'):
            elems['article:author'] = config.get('ogp_fb_author_url')
        body = entry['body']
        if isinstance(body, unicode):
            body = body.encode(config.get('blog_encoding', 'utf-8'))
        line = _DESC_REGEXP.sub('', body.split("\n")[0])
        elems['og:description'] = tools.escape_text(line)
        images = [x[1] for x in _IMG_REGEXP.findall(body)]
        if images:
            image = images[0]
            if not image.startswith('http'):
                image = urlparse.urljoin(config.get('base_url', ''), image)

    else:
        elems['og:type'] = 'blog'
        elems['og:title'] = config['blog_title']
        elems['og:url'] = config['base_url']
        description = config.get('blog_description')
        if description:
            elems['og:description'] = tools.escape_text(description)

    elems['og:site_name'] = config['blog_title']

    if image:
        elems['og:image'] = image
    else:
        elems['og:image'] = config.get('blog_image_url', _IMAGE_URL)

    data['ogp_tag'] = '\n'.join([_TAG_TEMPLATE % (key, elems[key])
                                 for key in elems])
