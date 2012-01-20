from __future__ import with_statement

from .storage_backend import StorageBackend


class TextBackend(StorageBackend):
    DEFAULT_FILE = 'tracker.txt'

    def __init__(self):
        self._connected = False
        self._tracked_urls = set()

    def already_visited_url(self, url, tracker_file=DEFAULT_FILE):
        if not self._tracked_urls:
            with open(tracker_file, 'r+') as tracker:
                self._tracked_urls = set([_.rstrip() for _ in
                                          tracker.readlines()])

        return url in self._tracked_urls

    def save_url(self, url, tracker_file=DEFAULT_FILE):
        self._tracked_urls.add(url)

        with open(tracker_file, 'a') as tracker:
            tracker.write(str(url) + "\n")

    def connect(self, filename=DEFAULT_FILE):
        fh = None
        try:
            fh = open(filename, 'a+')
            self._connected = True
        except Exception as e:
            self._connected = False
        finally:
            if fh:
                fh.close()

    def connected(self):
        return self._connected
