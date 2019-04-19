#!/usr/bin/env python
# -*- coding:utf-8 -*-

class pople:
    type = 'human'

    @property
    def default(self):
        temp = "I can from %s" %self.type
        return temp

    @default.setter
    def default(self, type):
        self.type = type

    def sex(self):
        self.name = 'jone'


# obj = pople()
# r = obj.default
# print(r)
# print(obj.type)

obj = pople()
r = obj.default
print(r)
obj.default = "123"
print(r)
