import httplib2
import sys

from HTMLParser import HTMLParseError

from BeautifulSoup import BeautifulSoup, SoupStrainer

from .pastesource import PasteSource


class PastebinSource(PasteSource):
    baseurl = 'http://pastebin.com'

    def new_urls(self, backend):
        http = httplib2.Http()
        status, response = http.request('http://pastebin.com/archive')
        product = SoupStrainer("td", {"class": "icon"})
        soup = BeautifulSoup(response, parseOnlyThese=product)

        for link in soup.findAll("a"):
            app = link["href"]
            if not backend.already_visited_url(self.full_url(app)):
                yield self, app

    def get_paste(self, path):
        http = httplib2.Http()
        status, response = http.request(self.full_url(path))
        try:  # wrap parser to avoid malformed error
            feast = BeautifulSoup(response,
                                parseOnlyThese=SoupStrainer("textarea"))
        except HTMLParseError as e:  # return a blank which will
            print >> sys.stderr, "failed on get_paste for path '%s': %s" % (
                    path, e)
            feast = ""

        return status, feast

    def full_url(self, path):
        return self.baseurl + path
