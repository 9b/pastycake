import argparse
import re
import sys
import time

from pastycake.sqlite_backend import SqliteBackend
from pastycake.text_backend import TextBackend
from pastycake.pastebin_source import PastebinSource
from pastycake.pastie_source import PastieSource
from pastycake.mailer import Mailer

DEFAULT_KEYWORDS = [
    'password',
    'hack',
]


def _parse_opts(args):
    opt_parser = argparse.ArgumentParser(
                                    description='harvest or snatch pastes')
    opt_parser.add_argument('-k', '--use_keyfile', nargs=1, metavar='KWFILE',
                            dest='kwfile', type=argparse.FileType('r'),
            help='read the keywords from KWFILE. if not given as an \
                  argument, then the built-in DEFAULT_KEYWORDS will be used.'
    )
    opt_parser.add_argument('-o', '--output', metavar='FILENAME',
                            dest='filename', action='store', default=None,
                            type=str,
                            help='specify a different output filename')
    opt_parser.add_argument('gather_mode', metavar='MODE', type=str,
                            choices=('harvest', 'snatch'),
            help='the mode to use. must be one of \'harvest\' or \'snatch\''
    )
    opt_parser.add_argument('add_keywords', metavar='KEYWORDS', nargs='*',
                        help='additional keywords to search for')
    opt_parser.add_argument('-a','--alert_email', metavar='EMAIL', type=str,
                            dest='alert_email', help='email to send alerts to', 
                            default=None, action='store'                       
    )

    return opt_parser.parse_args(args)


def _read_keywords(fhandle):
    return [_.rstrip() for _ in fhandle]


def fetch(storage, sources, keywords, email, store_match):
    search_re = re.compile('|'.join(keywords))

    for src in sources:
        for generator, path in src.new_urls(storage):
            status, data = generator.get_paste(path)
            full_url = generator.full_url(path)

            match = search_re.search(str(data))

            storage.save_url(full_url, match.group() if match and store_match
                             else match)

            if match:
                print '%s matched %s' % (full_url, match.group())

                if email:
                   email.sendmail(full_url,match.group())


def main(args=None):
    def _backend_or_exit(storage):
        storage.connect()
        if not storage.connected():
            print >> sys.stderr, "failed to open storage backend"
            sys.exit(1)
        return storage

    try:
        opts = _parse_opts(args)
    except IOError as e:
        print >> sys.stderr, "option error: %s" % e
        sys.exit(1)

    keywords = None
    if opts.kwfile:
        keywords = _read_keywords(opts.kwfile[0])
    else:
        keywords = DEFAULT_KEYWORDS

    sources = [
        PastebinSource(),
        PastieSource()
    ]

    email = None
    if opts.alert_email:
        email = Mailer(opts.alert_email)

    if opts.gather_mode == 'harvest':
        while True:
            fetch(_backend_or_exit(SqliteBackend(opts.filename)),
                  sources, keywords, email, store_match=True)
            time.sleep(5)
    elif opts.gather_mode == 'snatch':
        fetch(_backend_or_exit(TextBackend(opts.filename)),
              sources, keywords, email,store_match=False)
    else:
        print >> sys.stderr, "unknown gathering mode %s" % opts.gather_mode
        sys.exit(1)


if __name__ == '__main__':
    main()
