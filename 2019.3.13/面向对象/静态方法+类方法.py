#!/usr/bin/env python
# -*- coding:utf-8 -*-

class pople:
    type = 'human'

    @staticmethod
    def staticms(arg1, arg2):
        KEY = arg1
        VALUE = arg2
        print(KEY,VALUE)

    @classmethod
    def classms(cls):
        print("xxx",cls,type(cls))

    def sex(self):
        self.name = 'jone'

# obj = pople()

pople.classms()
# print(obj.type)
