from pastycake.mongodb_backend import MongoBackend
from pastycake.mailer import Mailer
from pastycake.pastie_source import PastieSource


backend = MongoBackend(host='127.0.0.3', username='abc',
                       password='chngeme')


def _my_awesome_kw_filter(text):
    #TODO: investigate why the file-level re import doesn't seem to work
    import re

    res = []
    tmp = re.search('username', text, re.I)
    if tmp:
        res.append(tmp.group())

    tmp = re.search('password', text, re.I)
    if tmp:
        res.append(tmp.group())

    tmp = re.search('p[0Oo]rn', text, re.I)
    if tmp:
        res = []

    return None if 2 != len(res) else ','.join(res)


keywords = ['foo', 'bar', _my_awesome_kw_filter]

listeners = [Mailer('foo@bar')]

sources = [PastieSource()]
