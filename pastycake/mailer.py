import smtplib
import socket
import sys

from email.mime.text import MIMEText

from pastebin_source import PastebinSource


class Mailer(object):
    def __init__(self, recv, sender=None):
        self._recv = recv
        self._sender = sender

    def get_paste_text(self, url):
        pb = PastebinSource()
        status, data = pb.get_paste(url)
        if data == '':
            data = "Failed to pull paste data"
        return data

    def sendmail(self, url, matcher):
        sender = self._sender or "pastycake@" + socket.gethostname()
        recv = self._recv
        subject = "[PastyCake] " + url + " matched " + matcher
        text = self.get_paste_text(url)

        try:
            text = str(text)
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
            sys.exit(1)
