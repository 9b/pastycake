import sys
import socket
import smtplib
import string
from pastebin_source import PastebinSource

class Mailer():
    def __init__(self,recv):
        self._recv = recv

    def get_paste_text(self,url):
        pb = PastebinSource()
        status, data = pb.get_paste(url)
        if data == '':
            data = "Failed to pull paste data"
        return data

    def sendmail(self,url,matcher):
        sender = "pastycake@" + socket.gethostname()
        recv = self._recv
        subject = "[PastyCake] " + url + " matched " + matcher
        text = self.get_paste_text(url)

        try:
            body = string.join((
                "From: %s" % sender,
                "To: %s" % recv,
                "Subject: %s" % subject,
                "",
                str(text)
            ), "\r\n")
        except:
            body = string.join((
                "From: %s" % sender,
                "To: %s" % recv,
                "Subject: %s" % subject,
                "",
                str("Failed to handle non-ascii code")
            ), "\r\n")

        server = smtplib.SMTP("localhost")
        try:
            server.sendmail(sender, recv, body)
            server.close()
        except Exception, e:
            print >> sys.stderr, "Unable to send email. Error: %s" % str(e)
            sys.exit(1)
