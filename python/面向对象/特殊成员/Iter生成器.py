#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 执行了iter方法



class Anna:
    def __iter__(self):
        yield 123


obj = Anna()

for i in obj:
    print(i)
