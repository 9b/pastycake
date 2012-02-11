import random
import re
import sys
import time

import louie as L

from pastycake.config import Config


#def fetch(storage, sources, keywords, store_match):
def fetch(conf_obj, store_match=True):
    search_re = re.compile('|'.join(conf_obj['keywords']))
    storage = conf_obj['backend']

    for src in conf_obj['sources']:
        for generator, path in src.new_urls(storage):
            status, data = generator.get_paste(path)

            #if 5xx or 4xx
            if status['status'][0] in ('4', '5'):
                #TODO better handling of timeouts
                print >> sys.stderr, "%s: %s. skipping" % (path,
                                                           status['status'])
                continue

            full_url = generator.full_url(path)

            match = search_re.search(str(data))

            storage.save_url(full_url,
                             match.group() if match and store_match else None)

            if match:
                L.send('match', generator, storage, match=match.group(),
                       url=full_url, data=data)


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
    conf['modefunc'](conf)


def harvest(conf=None):
    if not conf:
        sys.argv = sys.argv[0] + ['harvest'] + sys.argv[1:]
        return main()
    while True:
        fetch(conf)
        time.sleep(random.randint(5, 15))


def snatch(conf=None):
    if not conf:
        sys.argv = sys.argv[0] + ['snatch'] + sys.argv[1:]
        return main()
    fetch(conf, False)
