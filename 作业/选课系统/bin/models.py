#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pickle
import time


class Teacher:
    def __init__(self, name, age, admin):
        self.Name = name
        self.Age = age
        self.__assets = 0
        self.Create_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.Create_Admin = admin

    def gain(self, cost):
        self.__assets += cost

    def decrease(self, cost):
        self.__assets -= cost


class Admin:
    def __init__(self):
        self.Username = None
        self.Password = None

    def login(self, user, passwd):

        if self.Username == user and self.Password == passwd:
            return True
        else:
            return False

    def register(self, user, passwd):
        self.Username = user
        self.Password = passwd

        Path = 'db/admin/{db}'.format(db='db')
        pickle.dump(self, open(Path, 'xb'))
