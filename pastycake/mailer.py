import smtplib
import socket
import sys

import louie as L

from email.mime.text import MIMEText

from .notifier import Notifier


class Mailer(Notifier):
    def __init__(self, recv, sender=None):
        self._recv = recv
        self._sender = sender
        L.connect(self._handle_match, signal='match', sender=L.Any)

    def _handle_match(self, *args, **kwargs):
        self.sendmail(url=kwargs.get('url', ''),
                      matcher=kwargs.get('match', ''),
                      data=kwargs.get('data', ''))

    def sendmail(self, url, matcher, data):
        sender = self._sender or "pastycake@" + socket.gethostname()
        recv = self._recv
        subject = "[PastyCake] " + url + " matched " + matcher

        try:
            text = str(data)
        except:
            text = ''

        msg = MIMEText(text)
        msg['subject'] = subject
        msg['From'] = sender
        msg['To'] = recv

        server = smtplib.SMTP("localhost")
        try:
            server.sendmail(sender, recv, msg.as_string())
            server.close()
        except smtplib.SMTPException as e:
            print >> sys.stderr, "Unable to send email. Error: %s" % e
