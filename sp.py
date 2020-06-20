# coding: utf-8
"""
This plugin displays the 'sp.flav' flavour when accessed by a smartphone.
"""

__author__ = 'Junji NAKANISHI'
__email__ = 'jun-g at daemonfreaks.com'
__version__ = '0.2.20200620'
__url__ = 'http://www.daemonfreaks.com/'
__description__ = 'Displays the sp.flav flavour'
__license__ = 'MIT'


from datetime import datetime
from http.cookies import SimpleCookie


def verify_installation(request):
    return True


def cb_filelist(args):
    request = args['request']
    form = request.get_form()
    mode = form.getvalue('flav', '')

    is_sp = False
    res = request.get_response()

    if mode == 'html':
        expire = datetime(2001, 1, 1).strftime('%a, %d-%b-%Y %T GMT')
        res.add_header('Set-Cookie', 'mode=sp; path=/; expires=%s;' % (expire))
    elif mode == 'sp':
        res.add_header('Set-Cookie', 'mode=sp; path=/;')
        is_sp = True
    else:
        cs = request.http.get('HTTP_COOKIE', '')
        cookie = SimpleCookie()
        cookie.load(cs)
        if 'mode' in cookie and cookie['mode'].value == 'sp':
            is_sp = True

    if is_sp:
        data = request.get_data()
        data["flavour"] = "sp"
