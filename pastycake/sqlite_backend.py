import sqlite3 as S
import traceback

from sys import stderr

from .storage_backend import StorageBackend
from .keywords import KeywordStorage


class SqliteBackend(StorageBackend, KeywordStorage):
    DEFAULT_DB = 'urls.db'
    _DB_TABLES = '''
        CREATE TABLE matchers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_expression TEXT UNIQUE,
            enabled BOOL DEFAULT 1
        );
        CREATE TABLE urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE url_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url INTEGER REFERENCES urls(id) ON DELETE RESTRICT,
            matcher REFERENCES matchers(id) ON DELETE RESTRICT,
            matched TEXT
        );
    '''

    def __init__(self, filename=None):
        self._con = None
        self._filename = filename or self.DEFAULT_DB

    def _save_url(self, url):
        try:
            curs = self._con.cursor()
            curs.execute('INSERT OR IGNORE INTO urls(url) VALUES(?)', (url,))
            self._con.commit()
            res = curs.execute('SELECT id FROM urls WHERE url=?',
                            (url,)).fetchone()
            return res[0] if res else None
        except S.IntegrityError as e:
            print >> stderr, 'save url: %s' % e
            return None
        except S.Error as e:
            print >> stderr, 'save url: %s' % e
            return None

    def _save_matcher(self, matchname):
        try:
            curs = self._con.cursor()
            curs.execute('''INSERT OR IGNORE INTO matchers(match_expression)
                         VALUES(?)''', (matchname,))
            self._con.commit()
            res = curs.execute('''SELECT id FROM matchers WHERE
                               match_expression=?''', (matchname,)).fetchone()
            return res[0] if res else None
        except S.IntegrityError as e:
            print >> stderr, 'save matcher: %s' % e
            return None
        except S.Error as e:
            print >> stderr, 'save matcher: %s' % e
            return None

    def _save_urlmatch(self, urlid, matchid, text):
        curs = self._con.cursor()
        curs.execute('''INSERT OR IGNORE
                     INTO url_matches(url, matcher, matched)
                     VALUES(?, ?, ?)''', (urlid, matchid, text))
        self._con.commit()

    def already_visited_url(self, url):
        try:
            curs = self._con.cursor()
            res = curs.execute('SELECT * FROM urls WHERE url=?',
                                (url,))
            val = res.fetchone()
            return bool(val)
        except S.Error as e:
            print >> stderr, "failed to check url: %s" % e
            return False

    def save_url(self, url, matches=None):
        try:
            url_id = self._save_url(url)
            if not url_id:
                raise RuntimeError('failed to save or read url id (%s)' %
                                       url)
            if matches:
                for name, text in matches:
                    match_id = self._save_matcher(name)
                    if match_id:
                        self._save_urlmatch(url_id, match_id, text)

        except S.IntegrityError as e:
            print >> stderr, "issue 12 on github %r %s" % (url, e)
            traceback.print_exc(file=stderr)
        except S.Error as e:
            print >> stderr, "failed to save url: %s" % e
            raise
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
        try:
            self._con.executescript(self._DB_TABLES)
            self._con.commit()
        except S.OperationalError:
            #table already exists or we failed to lock the db
            pass

    # KeywordStorage implementation
    def _set_keyword_status(self, kwid, boolean):
        c = self._con.cursor()
        c.execute('UPDATE matchers SET enabled=? WHERE id=?', (boolean, kwid))
        self._con.commit()

    def enable_keyword(self, kw):
        kw_id = self._save_matcher(kw)
        self._set_keyword_status(kw_id, True)

    def disable_keyword(self, kw):
        kw_id = self._save_matcher(kw)
        self._set_keyword_status(kw_id, False)

    @property
    def available_keywords(self):
        c = self._con.cursor()
        return [_[0] for _ in
                    c.execute('SELECT match_expression FROM matchers'
                             ).fetchall()
               ]

    @property
    def current_keywords(self):
        c = self._con.cursor()
        return [_[0] for _ in c.execute(
                    'SELECT match_expression FROM matchers WHERE enabled=?',
                    (True,)
                ).fetchall()
                ]
