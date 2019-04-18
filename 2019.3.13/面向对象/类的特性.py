#!/usr/bin/env python
# -*- coding:utf-8 -*-

class pople:
    type = 'human'

    @property
    def default(self):
        temp = "I can from %s" %self.type
        return temp

    def sex(self):
        self.name = 'jone'

obj = pople()
r = obj.default
print(r)

# print(obj.type)
