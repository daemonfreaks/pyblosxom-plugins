"""
A Pyblosxom plugin to check whether there are some NG words in the comment.
"""

__author__ = "Junji NAKANISHI <daemonfreaks@gmail.com>"
__version__ = "0.2.20200620"
__url__ = 'https://github.com/daemonfreaks/pyblosxom-plugins/'
__description__ = 'NG words plugin for PyBlosxom'
__license__ = 'MIT'


from Pyblosxom import tools


def verify_installation(request):
    return True


def cb_comment_reject(args):
    comment = args["comment"]
    request = args["request"]
    config = request.get_configuration()
    http = request.get_http()

    for word in config.get("ngwords", []):
        for element in ('author', 'link', 'email', 'description'):
            if comment[element]:
                if word in comment[element]:
                    _write_log(http['REMOTE_ADDR'], comment['author'],
                               comment['description'], word)
                    return True

    return False


def _write_log(remote_host, author, comment, ngword):
    logger = tools.get_logger()
    logger.info('Comment rejected: {}@{}\n'
                'NG word: {}\n'
                '{}'.format(author, remote_host, ngword, comment))
