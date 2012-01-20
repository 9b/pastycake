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
_tracked_urls = set()


def clean(val):
    if type(val) is not str:
        val = str(val)
    val = re.sub(r'<.*?>', '', val)  # remove tags
    return val.strip()  # remove leading & trailing whitespace


def save_url(url, tracker_file=_DEFAULT_TRACKER_FILE):
    global _tracked_urls
    _tracked_urls.add(url)

    with open(tracker_file, 'a') as tracker:
        tracker.write(str(url) + "\n")


def already_visited_url(url, tracker_file=_DEFAULT_TRACKER_FILE):
    global _tracked_urls

    if not _tracked_urls:
        with open(tracker_file, 'r+') as tracker:
            _tracked_urls = set([_.rstrip() for _ in tracker.readlines()])

    return url in _tracked_urls


http = httplib2.Http()
status, response = http.request('http://pastebin.com/archive')
product = SoupStrainer("td", {"class": "icon"})
soup = BeautifulSoup(response, parseOnlyThese=product)

for link in soup.findAll("a"):
    app = link["href"]

    if not already_visited_url(app):
        save_url(app)
        tmper = base_url + app
        status, response = http.request(tmper)
        # appears to only have one textarea
        feast = BeautifulSoup(response,
                              parseOnlyThese=SoupStrainer("textarea"))
        m = re.search('|'.join(keywords), str(feast))

        if m:
            print tmper + " matched " + m.group()
