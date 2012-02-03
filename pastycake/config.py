import argparse
import imp
import sys

from .mailer import Mailer


def _read_keywords(fhandle):
    return [_.rstrip() for _ in fhandle]


def _create_arg_parser():
    opts = argparse.ArgumentParser(description='harvest or snatch pastes')
    opts.add_argument('-a', '--alert_email', metavar='EMAIL', type=str,
                        dest='alert_email', help='email to send alerts to',
                        default=None, action='store'
                        )
    opts.add_argument('-k', '--use_keyfile', metavar='KWFILE',
                        dest='kwfile', type=argparse.FileType('r'),
                        help='read the keywords from KWFILE. if not given \
                                as an argument, then the built-in \
                                DEFAULT_KEYWORDS will be used.'
                        )
    opts.add_argument('-o', '--output', metavar='FILENAME',
                        dest='filename', action='store', default=None,
                        type=str,
                        help='specify a different output filename'
                        )
    opts.add_argument('gather_mode', metavar='MODE', type=str,
                        choices=('harvest', 'snatch'),
                        help="the mode to use. must be one of 'harvest' \
                                or 'snatch'"
                        )
    opts.add_argument('add_keywords', metavar='KEYWORDS', nargs='*',
                        help='additional keywords to search for'
                        )
    return opts

class Config(dict):
    _DEFAULT_KEYWORDS = [
        'password',
        'hack',
    ]

    def __init__(self, defaults = None):
        super(Config, self).__init(defaults or dict())
        self._set_default_options()

    def _set_default_options(self):
        self['keywords'] = self._DEFAULT_KEYWORDS
        #TODO

    def parse_file(self, filename, format='py'):
        if format not in ('py', 'ini'):
            raise ValueError("invalid file format")
        if format == 'py':
            m = imp.new_module('pastycake_config')
            m.__file__ = filename

            try:
                execfile(filename, m.__dict__)
            except IOError as e:
                print >> sys.stderr, "Failed to parse config file %s: %s" % (
                    filename, e)
                return

            self.update(m.__dict__)
        elif format == 'ini':
            #TODO
            pass

    def have_an_argument(self, arguments=None):
        opts = _create_arg_parser()

        try:
            (vals, args) = opts.parse_args(arguments)
        except IOError as e:
            print >> sys.stderr, "failed to parse options: %s" % e
            sys.exit(1)

        if vals.kwfile:
            self['keywords'].update(_read_keywords(vals.kwfile[0]))

        if vals.alert_email:
            #TODO check if a mailer is already a listener and change
            # the receiver address instead
            self.listeners.append(Mailer(opts.alert_email))

        if vals.gather_mode not in ('harvest', 'snatch'):
            print >> sys.stderr, "unknown gathering mode %s" % vals.gather_mode
        self['gather'] = vals.gather_mode
        self['output.filename'] = vals.filename


