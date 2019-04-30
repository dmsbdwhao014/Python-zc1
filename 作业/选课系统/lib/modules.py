#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pickle
import sys
import time

sys.path.append(os.path.dirname((os.path.dirname(__file__))))
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
        path = os.path.join(settings.admin_db_dir, self.Username)
        if os.path.exists(path):
            return 2
        else:
            pickle.dump(self, open(path, 'xb'))
            return 4


class Student:
    def __init__(self):
        self.username = None
        self.password = None
        self.course_list = []
        self.study_dict = []

    def select_course(self, course_obj):
        self.course_list.append(course_obj)

    def study(self, course_obj):
        class_result = course_obj.have_lesson()

        if course_obj in self.study_dict.keys():
            self.study_dict[course_obj].append(class_result)
        else:
            self.study_dict[course_obj] = [class_result, ]

    def login(self, user, passswd):

        if self.username == user and self.password == passswd:
            return True
        else:
            return False

    def register(self, user, passwd):
        self.username = user
        self.password = passwd
        path = os.path.join(settings.student_db_dir, self.username)
        pickle.dump(self, open(path, 'xb'))


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
