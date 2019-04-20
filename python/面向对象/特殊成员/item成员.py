#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Anna:
    def __init__(self):
        print("init")

    def __call__(self, *args, **kwargs):
        print("call")
        return 11

    def __setitem__(self, key, value):
        print(key,value)
    def __getitem__(self, item):
        print(item)
    def __delitem__(self, key):
        print(key)

r = Anna()
r['ke']
r['k2'] = '1231'
del r['asdfasdfa']

