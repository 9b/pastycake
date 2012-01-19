import time
import httplib2
import re
import sqlite3 as sql
from BeautifulSoup import BeautifulSoup, SoupStrainer


#declare
db = "urls.db"
base_url = "http://pastebin.com"
keywords = ['password',
            'hack',
           ]


try:
    con = sql.connect(db)
except:
    print "Could not connect to " + db


def clean(val):
    if type(val) is not str:
        val = str(val)
    val = re.sub(r'<.*?>', '', val)  # remove tags
    return val.strip()  # remove leading & trailing whitespace


def save_url(url, matcher):
    cur = con.cursor()
    cur.execute("insert into urls(url,matcher) values(?,?)", [url, matcher])
    con.commit()


def already_visited_url(url):
    cur = con.cursor()
    cur.execute("select * from urls where url=?", [url])
    #fetchone() returns None if no result and that gets converted to False
    return bool(cur.fetchone())


def fetch():
    http = httplib2.Http()
    status, response = http.request('http://pastebin.com/archive')
    product = SoupStrainer("td", {"class": "icon"})
    soup = BeautifulSoup(response, parseOnlyThese=product)
    for link in soup.findAll("a"):
        app = link["href"]
        if not already_visited_url(app):
            tmper = base_url + app
            status, response = http.request(tmper)
            # appears to only have one textarea
            feast = BeautifulSoup(response,
                                  parseOnlyThese=SoupStrainer("textarea"))
            m = re.search('|'.join(keywords), str(feast))
            if m:
                print tmper + " matched " + m.group()
                save_url(app, str(m.group()))
            else:
                save_url(app, "")


if __name__ == "__main__":
    while(1):
        fetch()
        time.sleep(5)
