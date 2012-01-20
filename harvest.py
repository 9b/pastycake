import time
import httplib2
import re
import sys

#from BeautifulSoup import BeautifulSoup, SoupStrainer

import pastycake.db as db

from pastycake.pastebin_source import PastebinSource
from pastycake.pastie_source import PastieSource

#declare
keywords = ['password',
            'hack',
           ]

con = None


def init_db():
    global con
    con = db.connect_db() or sys.exit(1)
    db.create_tables(con)


def clean(val):
    if type(val) is not str:
        val = str(val)
    val = re.sub(r'<.*?>', '', val)  # remove tags
    return val.strip()  # remove leading & trailing whitespace


def fetch(sources):
    global con

    http = httplib2.Http()

    search_re = re.compile('|'.join(keywords))

    for src in sources:
        for generator, path in src.new_urls(con):
            status, data = generator.get_paste(path)
            full_url = generator.full_url(path)

            match = search_re.search(str(data))

            if match:
                print full_url + " matched " + match.group()
                db.save_url(con, full_url, str(match.group()))
            else:
                db.save_url(con, full_url, "")


if __name__ == "__main__":
    init_db()
    sources = [PastebinSource(),
               #PastieSource(),
              ]
    while(1):
        fetch(sources)
        time.sleep(5)
