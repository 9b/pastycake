from __future__ import with_statement

import re
import sys

from pastycake.pastebin_source import PastebinSource
from pastycake.text_backend import TextBackend


#declare
base_url = "http://pastebin.com"
keywords = ['password',
            'hack',
           ]


def clean(val):
    if type(val) is not str:
        val = str(val)
    val = re.sub(r'<.*?>', '', val)  # remove tags
    return val.strip()  # remove leading & trailing whitespace


def fetch(tracker, sources):
    search_re = re.compile('|'.join(keywords))

    for src in sources:
        for generator, path in src.new_urls(tracker):
            status, data = generator.get_paste(path)
            full_url = generator.full_url(path)

            match = search_re.search(str(data))

            tracker.save_url(full_url)

            if match:
                print full_url + " matched " + match.group()


if __name__ == '__main__':
    tracker = TextBackend()
    tracker.connect()
    tracker.connected() or sys.exit(1)

    sources = [PastebinSource(),
              ]

    fetch(tracker, sources)
