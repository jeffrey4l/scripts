#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author: Lei Zhang <zhang.lei.fly@gmail.com>
  
'''
A funny script about me
'''

def about_me(me):
    return me in ['python','linux','java','vim']

if __name__ == '__main__':  
    print about_me('java')
    print about_me('ja1va')
