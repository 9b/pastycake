import argparse
import imp
import os.path
import sys

from ConfigParser import ConfigParser

from pkg_resources import load_entry_point

from .mailer import Mailer
from .pastebin_source import PastebinSource
from .sqlite_backend import SqliteBackend
from .text_backend import TextBackend
from .cli_notifier import CliNotifier

from .pastesource import PasteSource
from .storage_backend import StorageBackend
from .notifier import Notifier


def _read_keywords(fhandle):
    return [_.rstrip() for _ in fhandle]


def load_ep_object(epname, section_name=None):
    def _do_load(package, section_name, epname):
        try:
            return load_entry_point(package, section_name, epname)
        except ImportError as e:
            #print >> sys.stderr, 'failed to load entry point %s: %s' % (
            #                                                       epname, e)
            return None

    if not section_name:
        return _do_load('pastycake', 'pastycake', epname) or \
               _do_load('pastycake', 'pastycake.ext', epname)
    else:
        return _do_load('pastycake', section_name, epname)


def _create_arg_parser():
    opts = argparse.ArgumentParser(description='harvest or snatch pastes')
    opts.add_argument('-a', '--alert_email', metavar='EMAIL', type=str,
                        dest='alert_email', help='email to send alerts to',
                        default=None, action='store'
                     )
    opts.add_argument('-c', '--config', metavar='CFG',
                        dest='config_fname', action='store', default=None,
                        help='load the config from file CFG. a file ending in \
                              .py(co)? will be treated as python source \
                              whereas a file ending in .ini or .cfg will \
                              be treated as ini-style.'
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

    def __init__(self, defaults=None):
        super(Config, self).__init__(defaults or dict())
        self._set_default_options()

    def _set_default_options(self):
        self['backend'] = SqliteBackend()
        self['keywords'] = self._DEFAULT_KEYWORDS
        self['notifiers'] = [CliNotifier()]
        self['modefunc'] = load_entry_point('pastycake', 'console_scripts',
                                            'pastycake-harvest')
        self['sources'] = [PastebinSource()]

    def _load_python_config(self, filename):
        m = imp.new_module('pastycake_config')
        m.__file__ = filename

        try:
            execfile(filename, m.__dict__)
        except IOError as e:
            print >> sys.stderr, "Failed to parse config file %s: %s" % (
                filename, e)
            return

        self.update(m.__dict__)

    def _load_ini_config(self, filename):
        def _map_section(conf, sectname):
            return dict([(opt, val) for opt, val in conf.items(sectname)])

        p = ConfigParser()
        p.read(filename)

        if p.has_section('backend'):
            tmp = _map_section(p, 'backend')

            if 'type' not in tmp.keys():
                raise LookupError('backend without type specified')

            tmp_obj = load_ep_object(tmp['type'])
            assert(issubclass(tmp_obj, StorageBackend))

            del tmp['type']

            self['backend'] = tmp_obj(tmp)

        if p.has_section('keywords'):
            kws = []
            for _ in filter(lambda x: x.startswith('file'),
                            p.options('keywords')):
                with open(p.get('keywords', _), 'r') as inkws:
                    kws += _read_keywords(inkws)

            kws = list(set(kws))
            if p.has_option('keywords', 'add') and \
               p.getboolean('keywords', 'add'):
                self['keywords'] += kws
            else:
                self['keywords'] = kws

        for _, _class in (('notifiers', Notifier), ('sources', PasteSource)):
            if p.has_section(_):
                tmp = []
                for opt in p.options(_):
                    tmp_obj = load_ep_object(p.get(_, opt))
                    assert(issubclass(tmp_obj, _class))

                    obj_opts = _map_section(p, opt) if p.has_section(opt) \
                                                    else {}
                    tmp.append(tmp_obj(obj_opts))

                assert(len(tmp))
                self[_] = tmp

    def parse_file(self, filename, format='py'):
        if format not in ('py', 'ini'):
            raise ValueError("invalid file format")
        if format == 'py':
            self._load_python_config(filename)
        elif format == 'ini':
            self._load_ini_config(filename)

    def parse_cli(self, arguments=None):
        opts = _create_arg_parser()

        try:
            vals = opts.parse_args(arguments)
        except IOError as e:
            print >> sys.stderr, "failed to parse options: %s" % e
            sys.exit(1)

        if vals.config_fname:
            extension = os.path.splitext(vals.config_fname)[1]

            if extension.startswith('.py'):
                extension = 'py'
            elif extension in ('.ini', '.cfg'):
                extension = 'ini'
            else:
                extension = 'py'
            self.parse_file(vals.config_fname, extension)

        if vals.kwfile:
            self['keywords'].update(_read_keywords(vals.kwfile[0]))

        if vals.alert_email:
            self['notifiers'].append(Mailer(opts.alert_email))

        if vals.gather_mode not in ('harvest', 'snatch'):
            print >> sys.stderr, "unknown gathering mode %s" % vals.gather_mode
        elif vals.gather_mode == 'harvest':
            self['modefunc'] = load_entry_point('pastycake', 'console_scripts',
                                                'pastycake-%s' %
                                                    vals.gather_mode)
        else:
            self['modefunc'] = load_entry_point('pastycake', 'console_scripts',
                                                'pastycake-snatch')
            self['backend'] = TextBackend()

        self['output.filename'] = vals.filename
