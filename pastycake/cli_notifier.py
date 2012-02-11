import louie as L

from .notifier import Notifier


class CliNotifier(Notifier):
    def __init__(self):
        L.connect(self._handle_match, signal='match', sender=L.Any)

    def _handle_match(self, *args, **kwargs):
        print '%s matched %s' % (kwargs.get('url', ''),
                                 kwargs.get('match', ''))
