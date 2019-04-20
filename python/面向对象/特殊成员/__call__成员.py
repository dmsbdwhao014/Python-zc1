#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Anna:
    def __init__(self):
        print("init")

    def __call__(self, *args, **kwargs):
        print("call")
        return 11


# obj = Anna()
# obj()
r = Anna()()
print(r)

