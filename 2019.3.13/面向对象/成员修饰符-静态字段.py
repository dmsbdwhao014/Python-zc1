#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Anna:
    firstname = 'zhou'
    __lastname = 'cheng'

    def __init__(self):
        pass

    def bella(self):
        print(Anna.__lastname)


obj = Anna()
obj.bella()
