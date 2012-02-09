from pastycake.mongodb_backend import MongoBackend
from pastycake.mailer import Mailer
from pastycake.pastie_source import PastieSource


backend = MongoBackend(host='127.0.0.3', username='abc',
                       password='chngeme')

keywords = ['foo', 'bar']

listeners = [Mailer('foo@bar')]

sources = [PastieSource()]
