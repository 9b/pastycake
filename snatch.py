from __future__ import with_statement
import httplib2
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer


#declare
base_url = "http://pastebin.com"
keywords = ['password',
            'hack',
           ]
_DEFAULT_TRACKER_FILE = 'tracker.txt'


def clean(val):
    if type(val) is not str:
        val = str(val)
    val = re.sub(r'<.*?>', '', val)  # remove tags
    return val.strip()  # remove leading & trailing whitespace


def save_url(url, tracker_file=_DEFAULT_TRACKER_FILE):
    tracker = open(tracker_file, "a")
    tracker.write(str(url) + "\n")
    tracker.close()


def check_url(url, tracker_file=_DEFAULT_TRACKER_FILE):
    tracker = open(tracker_file, "r+")
    lines = tracker.readlines()

    for line in lines:
        m = re.search(url, line)
        if m:
            return False
    return True


http = httplib2.Http()
status, response = http.request('http://pastebin.com/archive')
product = SoupStrainer("td", {"class": "icon"})
soup = BeautifulSoup(response, parseOnlyThese=product)

for link in soup.findAll("a"):
    app = link["href"]

    if check_url(app):
        save_url(app)
        tmper = base_url + app
        status, response = http.request(tmper)
        # appears to only have one textarea
        feast = BeautifulSoup(response,
                              parseOnlyThese=SoupStrainer("textarea"))
        m = re.search('|'.join(keywords), str(feast))

        if m:
            print tmper + " matched " + m.group()
