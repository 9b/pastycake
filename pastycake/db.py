from sys import stderr

import sqlite3 as S


DEFAULT_DB = 'urls.db'


def connect_db(path=DEFAULT_DB):
    try:
        return S.connect(path)
    except S.Error as e:
        print >> stderr, "failed to connect to db: %s" % e
        return None


def create_tables(sqlcon):
    _URL_TABLE = '''
    CREATE TABLE urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        matcher TEXT,
        viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''

    try:
        curs = sqlcon.cursor()
        curs.execute(_URL_TABLE)
        sqlcon.commit()
    except S.OperationalError:
        #table already exists or we failed to lock the db
        pass


def save_url(sqlcon, url, matcher):
    try:
        curs = sqlcon.cursor()
        curs.execute('INSERT INTO urls(url, matcher) VALUES(?, ?)',
                     (url, matcher))
        sqlcon.commit()
    except S.Error as e:
        print >> stderr, "failed to save url: %s" % e
        return False

    return True


def already_visited_url(sqlcon, url):
        try:
            curs = sqlcon.cursor()
            res = curs.execute('SELECT * FROM urls WHERE url=?', (url,))
            #returns None in case of absence and that gets converted to False
            return bool(res.fetchone())
        except S.Error as e:
            print >> stderr, "failed to check url: %s" % e
            return False
