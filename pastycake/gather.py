import random
import re
import sys
import time

import louie as L

from pastycake.config import Config
from pastycake.keywords import KeywordStorage


def _fetch_one(generator, path, keywords, storage, store_match):
    status, data = generator.get_paste(path)

    #if 5xx or 4xx
    if status['status'][0] in ('4', '5'):
        #TODO better handling of timeouts
        print >> sys.stderr, "%s: %s. skipping" % (path,
                                                    status['status'])
        return

    full_url = generator.full_url(path)
    match = None
    text = None
    name = None

    for kw in keywords:
        if hasattr(kw, '__call__'):
            text = kw(data)
            name = getattr(kw, '__name__')
        else:
            match = re.search(kw, data)
            name = kw
            text = match.group() if match else None

        if match:
            L.send('match', generator, storage, match=match.group(),
                    url=full_url, data=data)
            if store_match:
                storage.save_url(full_url, [(name, text), ])
            # stop after the first match
            break
    if not match and store_match:
        storage.save_url(full_url, None)


#def fetch(storage, sources, keywords, store_match):
def fetch(conf_obj, store_match=True):
    keywords = conf_obj['keywords']
    storage = conf_obj['backend']

    for src in conf_obj['sources']:
        for generator, path in src.new_urls(storage):
            _fetch_one(generator, path, keywords, storage, store_match)

    if isinstance(storage, KeywordStorage):
        conf_obj['keywords'] = storage.current_keywords


def main(args=None):
    def _backend_or_exit(storage):
        storage.connect()
        if not storage.connected():
            print >> sys.stderr, "failed to open storage backend"
            sys.exit(1)
        return storage

    def _load_conf(args=None):
        c = Config()
        c.parse_cli(args)
        return c

    conf = _load_conf(args)
    conf['backend'] = _backend_or_exit(conf['backend'])

    backend = conf['backend']
    if isinstance(backend, KeywordStorage):
        for _ in conf['keywords']:
            backend.enable_keyword(_ if not hasattr(_, '__call__')
                                   else _.__name__)
    conf['modefunc'](conf)


def harvest(conf=None):
    if not conf:
        sys.argv = [sys.argv[0]] + ['harvest'] + sys.argv[1:]
        return main()
    while True:
        fetch(conf)
        time.sleep(random.randint(5, 15))


def snatch(conf=None):
    if not conf:
        sys.argv = [sys.argv[0]] + ['snatch'] + sys.argv[1:]
        return main()
    fetch(conf, False)
