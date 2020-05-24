from Pyblosxom import tools, entries

TEMPLATE = """<script type="text/javascript" src="http://s.hatena.ne.jp/js/HatenaStar.js"></script>
<script type="text/javascript"><!--
Hatena.Star.Token = '%s';
Hatena.Star.EntryLoader.loadEntries = function() {
    return %s
}
//--></script>"""

TAG = """<span id="%s" class="%s"></span>"""


def verify_installation(request):
    return 1


def cb_prepare(args):
    request = args['request']
    config = request.getConfiguration()
    data = request.getData()
    token = config.get("hatenastar_token", "")
    star_class = config.get("hatenastar_star_class", "")
    comment_class = config.get("hatenastar_comment_class", "")
    values = list()
    for entry in data['entry_list']:
        star_id = '%s_star' % entry['tb_id']
        comment_id = '%s_comment' % entry['tb_id']
        value = dict()
        value['uri'] = "'%s/%s.html'" % (config['base_url'], entry['file_path'])
        value['title'] = "'%s'" % entry['title'].strip()
        value['star_container'] = 'document.getElementById(\'%s\')' % star_id
        value['comment_container'] = 'document.getElementById(\'%s\')' % comment_id
        values.append(value)
        entry['hatenastar_star'] = TAG % (star_id, star_class)
        entry['hatenastar_comment'] = TAG % (comment_id, comment_class)
    data['hatenastar_header'] = TEMPLATE % (token, _serialize_to_json(values))


def _serialize_to_json(obj):
    jsonvalues = list()
    for entry in obj:
        jsonentry = list()
        for key in entry.keys():
            #value = entry[key].replace("'", "\'")
            jsonentry.append("%s: %s" % (key, entry[key]))
        jsonvalues.append("{%s}" % (",\n".join(jsonentry)))
    return "[%s]" % (",\n".join(jsonvalues))

