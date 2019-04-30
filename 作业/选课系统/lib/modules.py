#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pickle
import time

from conf import settings


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


class Course:
    def __init__(self, name, cost, tearch, admin):
        self.course_name = name
        self.course_cost = cost
        self.tearch_name = tearch
        self.create_admin = admin
        self.Create_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


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
        if os.path.exists(settings.admin_db_dir + self.Username):
            return 2
        else:
            pickle.dump(self, open(settings.admin_db_dir + self.Username, 'xb'))
            return 4


def runcode(code):
    if code == 0:
        print("login successful.")
    elif code == 1:
        print("the adminstrator not exists.")
    elif code == 2:
        print("the adminstrator is exists.")
    elif code == 3:
        print("username or password is incorrect.")
    elif code == 4:
        print("administrator regesiter successful.")
    elif code == 5:
        print('tearch register successful.')
    elif code == 6:
        print("create  course successful.")
