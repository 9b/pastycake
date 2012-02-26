import httplib2

from lxml.html import parse

from .pastesource import PasteSource


class PastebinSource(PasteSource):
    baseurl = 'http://pastebin.com'

    def __init__(self, *args, **kwargs):
        pass

    def new_urls(self, backend):
        doc = parse('http://pastebin.com/archive').getroot()

        for link in doc.cssselect('.maintable tr td a'):
            app = link.get('href')
            if app.startswith('/archive/'):
                continue
            if not backend.already_visited_url(self.full_url(app)):
                yield self, app

    def get_paste(self, path):
        url = 'http://pastebin.com/raw.php?i=' + path[1:]
        http = httplib2.Http()
        try:
            res = http.request(url)
        except AttributeError as e:
            res = ({'status': '503'}, '')
        return res

    def full_url(self, path):
        return self.baseurl + path
