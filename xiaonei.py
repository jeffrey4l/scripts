#!/usr/bin/python
# coding=utf-8

# send xiaonei status 
import urllib2
import urllib
import cookielib
import re
import sys
import logging
import pdb
import json
import ConfigParser
import io
import threading
import time
import random
RENREN_LOGIN_URL="http://www.renren.com/Login.do"
RENREN_UPDATE_URL="http://status.renren.com/doing/update.do"
RENREN_LEAVE_URL="http://gossip.renren.com/gossip.do"
RENREN_PROFILE_URL="http://www.renren.com/profile.do?id=%s"
RENREN_MYFRIEND_URL="http://friend.renren.com/myfriendlistx.do"

def log(func):
    def wrapper(*args,**kwargs):
        logging.debug("Run into %s function" % func.__name__)
        ret = func(*args,**kwargs)
        logging.debug("Run out %s function" % func.__name__)
        if ret:
            return ret
    return wrapper

def new_thread(func):
    def _(*args,**kwargs):
        logging.debug("new threading")
        new_thread = threading.Thread(target=func,args = args,kwargs = kwargs)
        new_thread.start()
        time.sleep(2)
        logging.debug("The thread: %s is running" % (new_thread,))
    return _




class Renren(object):

    id_pattern = re.compile("XN\.user\.id = '(\d+)")
    token_pattern = re.compile("get_check:'(-?\d+)")

    @log
    def __init__(self,email,password):
        """"""
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.email = email
        self.password = password

    @log
    def login(self):
        """"""
        data = urllib.urlencode({"email":self.email,"password":self.password})
        ret = self.opener.open(RENREN_LOGIN_URL,data)
        content = ret.read()
        self.id = self.id_pattern.findall(content)[0]
        logging.debug("Get id: %s",self.id)
        self.token = self.token_pattern.findall(content)[0]
        logging.debug("Get token: %s",self.token)

    @log
    def send_status(self,msg):
        status={
                "c":msg,
                "isAtHome":"1",
                "publisher_form_ticket":self.token,
                "requestToken":self.token
                }
        data = urllib.urlencode(status)
        ret = self.opener.open(RENREN_UPDATE_URL,data)

    @log
    def leave_message(self,id,message):
        message={
                "body":message,
                "id":id,
                "cc":id,
                "headUrl":"",
                "largeUrl":"",
                "requestToken":self.token,
                "requestToken":self.token,
                "only_to_me":0,
                "color":"",
                "ref":"http://www.renren.com/getgossiplist.do",
                "mode":"",
                }
        data = urllib.urlencode(message)
        logging.debug("encoded leave message: %s",data)
        ret = self.opener.open(RENREN_LEAVE_URL,data)

        msg = json.JSONDecoder().decode(ret.read())
        if 0 == msg['code']:
            logging.debug("Send to %s successfully" % (id,))
        else:
            logging.debug("send to %s failed. error code: %s , error message: %s" % (id, msg['code'],msg['msg']))

    @log
    def get_myfriends(self):
        logging.debug("Try to open url:%s",RENREN_MYFRIEND_URL)
        ret = self.opener.open(RENREN_MYFRIEND_URL)
        content = ret.read()
        friends_pattern = re.compile(r'var friends=(.*);')
        friends = json.JSONDecoder().decode(friends_pattern.findall(content)[0])
        return friends

def main():
    config = ConfigParser.ConfigParser()
    try:
        config.read('setting.conf')
        EMAIL=config.get('default','username')
        PASSWORD=config.get('default','password')
    except:
        EMAIL=""
        PASSWORD=""
    rr = Renren(EMAIL,PASSWORD)
    rr.login()
    friends = rr.get_myfriends()
    cur = 0
    for friend in friends[cur:]:
        cur +=1
        logging.debug("sending message to %s (%d/%d)" % (friend['name'],cur,len(friends)))
        rr.leave_message(friend["id"],"Test %d" % (cur,))

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("cp936")
    logging.basicConfig(level=logging.DEBUG)

    main()
    #a = Test()
    #[a.test(i) for i in range(10)]

