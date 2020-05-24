from Pyblosxom import tools, entries
import time, os
def cb_filelist(args):
	request = args['request']
	data = request.getData()
	config = request.getConfiguration()

	allentries = tools.Walk(request, config['datadir'])

	i = 0
	recent = [ ]
	x = { }  
	for a in allentries:
		timetuple = tools.filestat(request, a)
		entrystamp = time.mktime(timetuple)
		tstamp = entrystamp
		a_path = a[len(config['datadir']):a.rfind(os.sep)]
		fn = a[a.rfind(os.sep)+1:a.rfind(".")]
		x[tstamp] = a

	e = x.keys()
	e.sort()
	e.reverse()
	f = e[0:10]
	for g in f:
		fn = x[g]
		e = entries.fileentry.FileEntry(request,fn,data['root_datadir'])
		#url="/%s/%s.html" % (e.get("absolute_path"), e.get("fn"))
		url="%s%s/%s.html" % (config["base_url"], e.get("absolute_path"), e.get("fn"))
		title=e.get("title")
		recent.append('* <a href="%s">%s</a>' % (url,title))
	data['recent'] = "<br/>".join(recent) 
