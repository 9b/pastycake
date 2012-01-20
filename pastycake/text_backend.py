from __future__ import with_statement

from .storage_backend import StorageBackend


class TextBackend(StorageBackend):
    DEFAULT_FILE = 'tracker.txt'

    def __init__(self, filename=None):
        self._connected = False
        self._tracked_urls = set()
        self._filename = filename or self.DEFAULT_FILE

    def already_visited_url(self, url):
        if not self._tracked_urls:
            with open(self._filename, 'r+') as tracker:
                self._tracked_urls = set([_.rstrip() for _ in
                                          tracker.readlines()])

        return url in self._tracked_urls

    def save_url(self, url, *args):
        self._tracked_urls.add(url)

        with open(self._filename, 'a') as tracker:
            tracker.write(str(url) + "\n")

    def connect(self):
        fh = None
        try:
            fh = open(self._filename, 'a+')
            self._connected = True
        except Exception as e:
            self._connected = False
        finally:
            if fh:
                fh.close()

    def connected(self):
        return self._connected
