"""
Creates a tagging environment and show tag cloud for pyblosxom

Tagging is like having an entry belong to multiple categories. For
example, an entry about Bike Riding in Pennsylvania can belong to
both Biking and Pennsylvania.

For more information on tags, please see sites such as technorati.com
and del.icio.us.

In your config file, create 4 settings:
py['tag_url']
py['pretext']
py['posttext']
py['tagsep']

The default tag_url should be set to http://yoursite/tags/, but you can also
set it to something like http://technorati.com/tags/.  Please make sure to
have the trailing slash.

The pretext and posttext will appear on your webpage surrounding your
tags and tagsep will note what to seperate the tags by.

So, for example, if I have
py['pretext'] = '<span class="tags">Tags '
py['posttext'] = '</span>'
py['tagsep'] = ', '

Then it would appear like:

    <span class="tags">Tags: biking, pennsylvania</span>

Why not just put the text in a template? Because if you don't want to tag
an entry, this would look goofy:

    Tags: (nothing)

Finally, add a meta-data tag to your entries:

    #tags biking,pennsylvania

comma, no space.


If you choose to set your tag_url to
http://yoursite/tags/, you will be able to do a search
for all tagged items like so:

    http://yoursite/tags/biking

Questions, comments, and fixes can be sent to joe@terrarum.net

** support for searching "untagged" tag hacked in by Timothy C. Fanelli -
10/22/05 **
    Tim made the following changes:
    It now filters out files that do not have a .txt extension -- this may
    or may not be generally desirable, as some other plugins allow
    different extensions for entries (e.g., portico looks for .port files,
    which might want to be tagged.)

    Also, I modified it to allow searching for "untagged" entries, using
    $tag_url/untagged -- it'l return entries which have no #tag meta
    entry. This was useful because I was completely replacing my
    categories with tags, and have a large "general" category which I
    didn't want to be bothered with.

        10/24 -
           1. Updated file filter hack to support config propery
              'taggable_files'

              Set py[ 'taggable_files' ] = [ "txt", "port", ... ]
              To support tagging of entries with those file extensions.
              Defaults to tag just entries with "txt" files.

           2. cb_fileset now returns entries sorted by date with most current
              first.

Original authors:

- Joe Topjian <joe@terrarum.net>
- shunuhs - shunuhs.jp at gmail dot com

"""

__author__ = 'Junji NAKANISHI <jun-g@daemonfreaks.com>'
__version__ = 'v0.1.20200528'
__url__ = 'http://github.com/daemonfreaks/pyblosxom-plugins/'
__description__ = "show tags cloud"


import os
import re
import sys

from Pyblosxom import entries, tools


def verify_installation(request):
    config = request.get_configuration()
    if 'tag_url' not in config:
        print('missing tag_url for tags.py and pytagcloud.py.')
        return 0
    return 1


def cb_filelist(args):
    request = args['request']
    config = request.get_configuration()
    data = request.get_data()
    new_files = []

    tagfileswithext = ["txt", "rst"]
    if 'taggable_files' in config:
        tagfileswithext = config['taggable_files']

    ignore_directories = []
    if 'ignore_directories' in config:
        ignore_directories = config['ignore_directories']

    m = re.compile(r'^%s' % config['tag_url']).match(data['url'])
    if m:
        tag = re.sub("%s" % config['tag_url'], '', data['url'])
        for root, dirs, files in os.walk(config['datadir']):
            for x in files:
                m = re.compile(r'.*\.([^.]+)$').search(x)
                if m and m.group(1) in tagfileswithext:
                    entry_location = root + "/" + x
                    directory = os.path.dirname(entry_location)
                    if os.path.split(directory)[1] in ignore_directories:
                        continue
                    contents = open(entry_location, 'r').read()
                    m = re.compile(r'\n#tags\s+(.*)\n').search(contents)
                    if (m and tag in m.group(1).split(',')) \
                       or (not m and tag == 'untagged'):
                        tmpentry = entries.fileentry \
                                   .FileEntry(request, entry_location,
                                              data['root_datadir'])
                        new_files.append((tmpentry._mtime, tmpentry))

    if new_files:
        new_files.sort()
        new_files.reverse()

        myentries = []
        for myentry in new_files:
            myentries.append(myentry[1])
        return myentries


def cb_story(args):
    request = args['request']
    config = request.get_configuration()
    entry = args['entry']
    if 'tags' in entry:
        formatted_tags = []
        temp_tags = []
        formatted_tags.append(config['pretext'])
        tags = [t.strip() for t in entry.get("tags", "").split(',')]

        for tag in tags:
            temp_tags.append('<a href="%s%s" rel="tag">%s</a>' % (
                             config['tag_url'], tag, tag))

        formatted_tags.append(config['tagsep'].join(temp_tags))
        formatted_tags.append(config['posttext'])
        entry["tags"] = " ".join(formatted_tags)


class TagCloud:

    def __init__(self, request):
        self._request = request
        self._tags = ''

    def __str__(self):
        return self.get_tag_cloud()

    def get_tag_cloud(self):
        if not self._tags:
            self._tags = self.generate_tag_cloud()
        return self._tags

    def generate_tag_cloud(self):
        config = self._request.get_configuration()
        root = config['datadir']

        tag_url = config.get('tag_url', '')
        elist = tools.walk(self._request, root)

        tags_dic = {}
        for i in elist:
            f = open(i, 'r')
            contents = f.read()
            f.close()

            m = re.search('\n#tags (.*?)\n', contents, re.M | re.S)
            if m:
                tags_str = m.group(1)
                tags_list = tags_str.split(',')
                for j in tags_list:
                    try:
                        tags_dic[j] += 1
                    except KeyError:
                        tags_dic[j] = 1

        output = ''

        tags_sum = sum(tags_dic.values())

        pretext = '<a title="%s posts" class="%s" href="'
        posttext = '</a>'

        for i in sorted(tags_dic):
            count = tags_dic[i]
            percent = count / float(tags_sum)
            if percent >= 0.2:
                percent = "twenty"
            elif percent >= 0.1:
                percent = "ten"
            elif percent >= 0.05:
                percent = "five"
            elif percent >= 0.01:
                percent = "one"
            else:
                percent = "zero"
            output += pretext % (count, percent) + tag_url + i + '">' + i
            output += posttext + '&nbsp;\n'
        return output


def cb_prepare(args):
    request = args['request']
    data = request.get_data()
    tc = TagCloud(request)
    data['tagcloud'] = tc.get_tag_cloud()
