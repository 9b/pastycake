import sys
import socket
import smtplib
import string

class Mailer():
    def __init__(self,recv):
        self._recv = recv

    def get_paste_text(url):
        raise NotImplemented()

    def sendmail(self,url,matcher):
        sender = "pastycake@" + socket.gethostname()
        recv = self._recv
        subject = "[PastyCake] " + url + " matched " + matcher
        text = "NT"

        body = string.join((
            "From: %s" % sender,
            "To: %s" % recv,
            "Subject: %s" % subject,
            "",
            text
        ), "\r\n")

        server = smtplib.SMTP("localhost")
        try:
            server.sendmail(sender, recv, body)
            server.close()
        except Exception, e:
            print >> sys.stderr, "Unable to send email. Error: %s" % str(e)
            sys.exit(1)
