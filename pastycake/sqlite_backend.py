import sqlite3 as S
import traceback

from sys import stderr

from .storage_backend import StorageBackend


class SqliteBackend(StorageBackend):
    DEFAULT_DB = 'urls.db'

    def __init__(self, filename=None):
        #self._visited_urls = set()
        self._con = None
        self._filename = filename or self.DEFAULT_DB

    def already_visited_url(self, url):
        #if url not in self._visited_urls:
        try:
            curs = self._con.cursor()
            res = curs.execute('SELECT * FROM urls WHERE url=?',
                                (url,))
            val = res.fetchone()
            return bool(val)
            #if val:
            #    self._visited_urls.add(val)
        except S.Error as e:
            print >> stderr, "failed to check url: %s" % e
            return False
        #return url in self._visited_urls

    def save_url(self, url, match_text=None):
        match_text = match_text or ''
        try:
            curs = self._con.cursor()
            curs.execute('INSERT INTO urls(url, matcher) VALUES(?, ?)',
                        (url, match_text))
            self._con.commit()
            #self._visited_urls.add(url)
        except S.IntegrityError as e:
            print >> stderr, "issue 12 on github %r %s" % (url, e)
            traceback.print_exc(file=stderr)
        except S.Error as e:
            print >> stderr, "failed to save url: %s" % e
            return False

        return True

    def connect(self):
        try:
            self._con = S.connect(self._filename)
            self._create_tables()
        except S.Error as e:
            print >> stderr, "failed to connect to db: %s" % e
            self._con = None

    def connected(self):
        return bool(self._con)

    def _create_tables(self):
        _URL_TABLE = '''
        CREATE TABLE urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            matcher TEXT,
            viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''

        try:
            curs = self._con.cursor()
            curs.execute(_URL_TABLE)
            self._con.commit()
        except S.OperationalError:
            #table already exists or we failed to lock the db
            pass
