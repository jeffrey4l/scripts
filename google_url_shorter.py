#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author: Lei Zhang <zhang.lei.fly@gmail.com>
 
'''
Here is a simple wrapper about google short url api.  It is based on the http 
api. 

The useage of google short url api:

$curl https://www.googleapis.com/urlshortener/v1/url   -H 'Content-Type:\
        application/json'   -d '{"longUrl": "http://www.google.com/abcdefght"}'
{
    "kind": "urlshortener#url",
    "id": "http://goo.gl/pnfCg",
    "longUrl": "http://www.google.com/abcdefght"
}
'''
import urllib2
import json
import logging

LOG = logging.getLogger(__name__)


def google_url_shortener(url):
    SHORTENER_URL='https://www.googleapis.com/urlshortener/v1/url'
    HEADERS = {'Content-Type':'application/json'}
    data = json.dumps({'longUrl':url})
    req = urllib2.Request(SHORTENER_URL,data,HEADERS)
    try:
        response = urllib2.urlopen(req)
        shortener_url = response.read()
        shortener_url = json.loads(shortener_url)
        return shortener_url
    except:
        LOG.exception('Can not get the shorter url:%s',url)

if __name__ == '__main__':
    print google_url_shortener('http://www.google.com/')

