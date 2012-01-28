import sys

from datetime import datetime as dt

try:
    import pymongo as M
except ImportError:
    print >> sys.stderr, "This backend requires pymongo to be installed"

from .storage_backend import StorageBackend


class MongoBackend(StorageBackend):
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 27017
    DEFAULT_DB = 'pastycake'

    def __init__(self, db_name=DEFAULT_DB, host=DEFAULT_HOST,
                 port=DEFAULT_PORT):
        self._db_name = db_name
        self._host = host
        self._port = port
        self._connected = False

    def already_visited_url(self, url):
        return bool(self._db.posts.find({'url': url}).count())

    def save_url(self, url, match_text=None, rec=0):
        def _do_save_url(self, url, match_text):
            self._db.posts.insert(
                {
                    'url': url,
                    'matches': match_text,
                    'visited': dt.utcnow(),
                }
            )
        try:
            _do_save_url(self, url, match_text)
            return
        except M.errors.PyMongoError as e:
            print >> sys.stderr, 'eror saving url: %s' % e

        # let's try again in case that the cursor timed out
        if not rec:
            self.connect()
            if self.connected():
                self.save_url(url, match_text, rec + 1)

    def connect(self):
        try:
            self._con = M.Connection(self._host, self._port)
            self._db = self._con[self._db_name]
            self._connected = True
        except M.errors.PyMongoError as e:
            print >> sys.stderr, "failed to connect: %s" % e
            self._connected = False

    def connected(self):
        return self._connected
