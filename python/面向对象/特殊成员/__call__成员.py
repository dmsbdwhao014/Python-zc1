#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 对象后加（）,执行类的call方法

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

