import httplib2

from BeautifulSoup import BeautifulSoup, SoupStrainer

from .pastesource import PasteSource
#from .db import already_visited_url


class PastieSource(PasteSource):
    baseurl = 'http://pastie.org'

    def new_urls(self, backend):
        http = httplib2.Http()
        status, response = http.request('http://pastie.org/pastes')
        product = SoupStrainer("div", {"class": "pastePreview"})
        soup = BeautifulSoup(response, parseOnlyThese=product)

        for link in soup.findAll("a"):
            app = link["href"]

            if not backend.already_visited_url(app):
                yield self, app

    def get_paste(self, path):
        http = httplib2.Http()
        status, response = http.request(path + '/text')
        return status, response

    def full_url(self, path):
        return path
