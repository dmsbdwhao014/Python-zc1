#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 静态方法可以继承，但是不能在派生类中访问基类的静态方法

class Anna:
    firstname = 'zhou'
    __lastname = 'cheng'

    def __init__(self):
        self.__name = 'zhoucheng'

    def bella(self):
        print(self.__lastname)


class cristina(Anna):
    def bella1(self):
        print(self.__name)


obj = cristina()
obj.bella()
