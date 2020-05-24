"""
Check to ng words in comment for PyBlosxom.
"""
__author__      = "Junji NAKANISHI <daemonfreaks@gmail.com>"
__version__     = "0.1"

from Pyblosxom import tools

def verify_installation(request):
    return 1

def cb_comment_reject(args):
    request = args["request"]
    config = request.getConfiguration()
    comment = args["comment"]

    for word in config.get("ngwords", []):
        if word in comment["description"]:
            http = request.getHttp()
            logger = tools.getLogger()
            logger.info('Comment rejected from %s:\n%s: %s' % (http['REMOTE_ADDR'],
                                                               comment["author"],
                                                               comment["description"]))
            return 1
    if "http" in comment["author"]:
        http = request.getHttp()
        logger = tools.getLogger()
        logger.info('Comment rejected from %s:\n%s: %s' % (http['REMOTE_ADDR'],
                                                           comment["author"],
                                                           comment["description"]))
        return 1 

    if comment["link"]:
        http = request.getHttp()
        logger = tools.getLogger()
        logger.info('Comment rejected from %s:\n%s: %s' % (http['REMOTE_ADDR'],
                                                           comment["author"],
                                                           comment["link"]))
        return 1

    if comment["email"]:
        http = request.getHttp()
        logger = tools.getLogger()
        logger.info('Comment rejected from %s:\n%s: %s' % (http['REMOTE_ADDR'],
                                                           comment["author"],
                                                           comment["email"]))
        return 1

    if comment["link"]:
        http = request.getHttp()
        logger = tools.getLogger()
        logger.info('Comment rejected from %s:\n%s: %s' % (http['REMOTE_ADDR'],
                                                           comment["author"],
                                                           comment["link"]))
        return 1
    return 0
