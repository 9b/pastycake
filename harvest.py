import time
import httplib2
import re
import sys

from BeautifulSoup import BeautifulSoup, SoupStrainer

import pastycake.db as db

#declare
base_url = "http://pastebin.com"
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


def fetch():
    global con

    http = httplib2.Http()
    status, response = http.request('http://pastebin.com/archive')
    product = SoupStrainer("td", {"class": "icon"})
    soup = BeautifulSoup(response, parseOnlyThese=product)

    for link in soup.findAll("a"):
        app = link["href"]

        if not db.already_visited_url(con, app):
            tmper = base_url + app
            status, response = http.request(tmper)
            # appears to only have one textarea
            feast = BeautifulSoup(response,
                                  parseOnlyThese=SoupStrainer("textarea"))
            m = re.search('|'.join(keywords), str(feast))

            if m:
                print tmper + " matched " + m.group()
                db.save_url(con, app, str(m.group()))
            else:
                db.save_url(con, app, "")


if __name__ == "__main__":
    init_db()
    while(1):
        fetch()
        #time.sleep(5)
        time.sleep(15)
