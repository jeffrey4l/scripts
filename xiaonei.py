#!/usr/bin/python
# coding=utf-8

# send xiaonei status 
import urllib2
import urllib
import cookielib
import re
import sys
RENREN_LOGIN_URL="http://www.renren.com/Login.do"
RENREN_UPDATE_URL="http://status.renren.com/doing/update.do"

class Renren(object):

    id_pattern = re.compile("(?<=XN\.user\.id = \')\d+")
    token_pattern = re.compile("(?<=get_check:\')-?\d+")

    def __init__(self,email,password):
        """"""
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.email = email
        self.password = password

    def _login(self):
        """"""
        data = urllib.urlencode({"email":self.email,"password":self.password})
        ret = self.opener.open(RENREN_LOGIN_URL,data)
        content = ret.readlines()
        for line in content:
            _id = self.id_pattern.findall(line)
            _token = self.token_pattern.findall(line)

            if not getattr(self,"token",False) and _token is not None and len(_token) > 0:
                self.token = _token[0]

            if not getattr(self,"id",False) and _id is not None  and len(_id) > 0:
                self.id = _id[0]

    def send_message(self,msg):
        try:
             getattr(self,"token") 
        except:
            self._login()

        status={
                "c":msg,
                "isAtHome":"1",
                "publisher_form_ticket":self.token,
                "requestToken":self.token
                }
        data = urllib.urlencode(status)
        ret = self.opener.open(RENREN_UPDATE_URL,data)

if __name__ == "__main__":
    EMAIL=""
    PASSWORD=""
    rr = Renren(EAMIL,PASSWORD)
    for arg in sys.argv[1:]:
        print rr.send_message(arg)
