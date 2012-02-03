import argparse
import random
import re
import sys
import time

import louie as L

from pastycake.sqlite_backend import SqliteBackend
from pastycake.text_backend import TextBackend
from pastycake.pastebin_source import PastebinSource
from pastycake.pastie_source import PastieSource
from pastycake.mailer import Mailer


def fetch(storage, sources, keywords, store_match):
    search_re = re.compile('|'.join(keywords))

    for src in sources:
        for generator, path in src.new_urls(storage):
            status, data = generator.get_paste(path)

            #if 5xx or 4xx
            if status['status'][0] in ('4', '5'):
                #TODO better handling of timeouts
                print >> sys.stderr, "%s. skipping" % status['status']
                continue

            full_url = generator.full_url(path)

            match = search_re.search(str(data))

            storage.save_url(full_url,
                             match.group() if match and store_match else None)

            if match:
                print '%s matched %s' % (full_url, match.group())
                L.send('match', generator, storage, match=match.group(),
                       url=full_url, data=data)


def main(args=None):
    def _backend_or_exit(storage):
        storage.connect()
        if not storage.connected():
            print >> sys.stderr, "failed to open storage backend"
            sys.exit(1)
        return storage

    keywords = None
    sources = [
        PastebinSource(),
        PastieSource()
    ]


if __name__ == '__main__':
    main()
