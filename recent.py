# coding: utf-8
"""
recent.py

This plugin provides a list of recent 10 entries in the `recent` variable.
"""

__author__ = 'Junji NAKANISHI <jun-g@daemonfreaks.com>'
__version__ = 'version 0.1.20200525'
__url__ = 'https://github.com/daemonfreaks/pyblosxom-plugins'
__description__ = 'This is a PyBlosxom plugin that provides recent entry list'

import time

from Pyblosxom import tools, entries


def cb_filelist(args):
    request = args['request']
    data = request.getData()
    config = request.getConfiguration()

    allentries = tools.Walk(request, config['datadir'])

    entries_by_time = {}
    for entry in allentries:
        timetuple = tools.filestat(request, entry)
        entrystamp = time.mktime(timetuple)
        entries_by_time[entrystamp] = entry

    times = sorted(entries_by_time.keys())
    times.reverse()
    times = times[0:10]

    recent = []
    for entry_time in times:
        entry = entries_by_time[entry_time]
        file_entry = entries.fileentry.FileEntry(request, entry,
                                                 data['root_datadir'])
        url = '%s%s/%s.html' % (config['base_url'],
                                file_entry.get('absolute_path'),
                                file_entry.get('fn'))
        title = file_entry.get('title')
        recent.append('<li><a href="%s">%s</a></li>' % (url, title))
    data['recent'] = '<ul id="recententries">\n%s\n</ul>' % ('\n'.join(recent))
