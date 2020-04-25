# coding: utf-8
"""
If Pyblosxom is rendering some entries, then this populates the 
``entry_title`` variable for the header template.
"""

__author__ = 'Junji NAKANISHI'
__email__ = 'jun-g at daemonfreaks dot com'
__version__ = '2013-09-23'
__url__ = 'http://www.daemonfreaks.com/'
__description__ = 'Puts entries title in page title.'
__license__ = 'MIT'


def verify_installation(request):
    return True


def cb_head(args):
    req = args["request"]
    entry = args["entry"]

    data = req.get_data()
    entry_list = data.get("entry_list", [])
    if len(entry_list) != 1:
        config = req.get_configuration()
        tmpl = config.get("entry_title_template", ":: %(title)s")
        path = data['pi_bl'].lstrip('/')
        entry["entry_title"] = (path and tmpl % {"title": path})

    return args

