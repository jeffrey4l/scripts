#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author: Lei Zhang <zhang.lei.fly@gmail.com>

import pdb
import unittest
 
class ParseQuery(object):

    start=0
    offset=0
    quote = False

    def __init__(self,query):
        self._query = query.strip()

    def __iter__(self):
        return self

    def next(self):
        while(True):
            if self.offset >= len(self._query):
                raise StopIteration()
            char = self._query[self.offset]
            if self.offset == self.start+1 and char in [' ','\t']:
                pdb.set_trace()
                self.start=self.offset
                self.offset=self.start+1
            elif not self.quote and char not in [u' ',u'"']:
                self.offset+=1
            elif char == u' ' and not self.quote:
                return self._word()
            elif char != u'"' and self.quote:
                self.offset +=1
            elif char == u'"' and not self.quote:
                self.quote = True
                self.offset += 1
            elif char == u'"' and self.quote:
                self.quote = False
                self.offset+=1
            if self.offset == len(self._query):
                return self._word()

    def _word(self):
        word = self._query[self.start:self.offset]
        self.start = self.offset + 1
        self.offset = self.start
        return word
    
    def __repr__(self):
        return "%s\n[%d,%d]" % (self._query,
                self.start,self.offset)
    

class ParseQueryTest(unittest.TestCase):

    def test_success(self):
        query = u'test author:zhanglei project:"solr - Apache"'
        parse = ParseQuery(query)
        self.assertEqual(list(parse),
                [u'test',u'author:zhanglei',u'project:"solr - Apache"'])
        query = u'author:"zhanglei" project:"solr - Apache" test'
        parse = ParseQuery(query)
        self.assertEqual(list(parse),
                [u'author:"zhanglei"',u'project:"solr - Apache"',u'test'])
        query = u'author:"zhanglei" project:"solr - Apache test'
        parse = ParseQuery(query)
        self.assertEqual(list(parse),
                [u'author:"zhanglei"',u'project:"solr - Apache test'])

        query = u'  author:"zhang lei"     project:"test"'
        parse = ParseQuery(query)
        self.assertEqual(list(parse),
                [u'author:"zhang lei"',u'project:"test"'])
        

if __name__ == '__main__':
    unittest.main()
