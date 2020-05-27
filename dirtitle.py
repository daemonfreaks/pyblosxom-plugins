# coding: utf-8
"""
If Pyblosxom is rendering some entries, then this populates the
``entry_title`` variable for the header template.
"""

__author__ = 'Junji NAKANISHI <jun-g@daemonfrekas.com>'
__version__ = '0.1.20200527'
__url__ = 'https://github.com/daemonfreaks/pyblosxom-plugins/'
__description__ = 'Puts entries title in page title.'
__license__ = 'MIT'


def verify_installation(request):
    return True


def cb_head(args):
    entry = args['entry']
    req = args['request']
    data = req.get_data()
    entry_list = data.get('entry_list', [])
    if len(entry_list) > 1:
        config = req.get_configuration()
        tmpl = config.get('entry_title_template', ':: %(title)s')
        path = data['pi_bl'].lstrip('/')
        entry['entry_title'] = (path and tmpl % {'title': path})
    return args
