import time
import re
import sys

#from BeautifulSoup import BeautifulSoup, SoupStrainer

from pastycake.sqlite_backend import SqliteBackend

from pastycake.pastebin_source import PastebinSource
from pastycake.pastie_source import PastieSource

#declare
keywords = ['password',
            'hack',
           ]

db = None


def init_db():
    global db
    db = SqliteBackend()
    db.connect()
    db.connected() or sys.exit(1)


def clean(val):
    if type(val) is not str:
        val = str(val)
    val = re.sub(r'<.*?>', '', val)  # remove tags
    return val.strip()  # remove leading & trailing whitespace


def fetch(sources):
    global db

    search_re = re.compile('|'.join(keywords))

    for src in sources:
        for generator, path in src.new_urls(db):
            status, data = generator.get_paste(path)
            full_url = generator.full_url(path)

            match = search_re.search(str(data))

            if match:
                print full_url + " matched " + match.group()
            db.save_url(full_url, match.group() if match else match)


if __name__ == "__main__":
    init_db()
    sources = [PastebinSource(),
               #PastieSource(),
              ]
    while(1):
        fetch(sources)
        time.sleep(5)
