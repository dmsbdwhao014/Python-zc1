#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Anna:
    Justname = 'Iloveit'

    def __init__(self):
        print("init")

    def __call__(self, *args, **kwargs):
        print("call")
        return 11

    def __setitem__(self, key, value):
        print(key, value, type(key), "setitem")
    def __getitem__(self, item):
        print(item, type(item), "getitem")
    def __delitem__(self, key):
        print(key, type(key), "delitem")


#
r = Anna()  # __init__
# r()                     #__call__
# r['ke']                 #getitem
# r['k2'] = '1231'       #setitem
# del r['asdfasdfa']    #delitem

# r[1:5]    #getitem
# r[1:5:2] = [11,2,3,45,5,6,6,7,8,9,1231] #setitem
# del r[1:3]  #delitem
print(r.__dict__)
print(Anna.__dict__)
