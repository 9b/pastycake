import time
import re
import sys

from pastycake.pastebin_source import PastebinSource
from pastycake.pastie_source import PastieSource
from pastycake.sqlite_backend import SqliteBackend

#declare
keywords = ['password',
            'hack',
           ]

def clean(val):
    if type(val) is not str:
        val = str(val)
    val = re.sub(r'<.*?>', '', val)  # remove tags
    return val.strip()  # remove leading & trailing whitespace


def fetch(db, sources):
    search_re = re.compile('|'.join(keywords))

    for src in sources:
        for generator, path in src.new_urls(db):
            status, data = generator.get_paste(path)
            full_url = generator.full_url(path)

            match = search_re.search(str(data))

            if match:
                print full_url + " matched " + match.group()
            db.save_url(full_url, match.group() if match else match)


if __name__ == "__main__":
    db = SqliteBackend()
    db.connect()
    db.connected() or sys.exit(1)

    sources = [PastebinSource(),
               #PastieSource(),
              ]
    while(1):
        fetch(db, sources)
        time.sleep(5)
