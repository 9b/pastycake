import httplib2

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
        # appears to only have one textarea
        feast = BeautifulSoup(response,
                                parseOnlyThese=SoupStrainer("textarea"))
        return status, feast

    def full_url(self, path):
        return self.baseurl + path
