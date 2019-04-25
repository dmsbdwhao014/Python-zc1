#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pickle

from lib import modules


def Create_tearch(admin):
    tearch_list = []
    while True:
        name = input("请输入老师名:")
        if name == 'q':
            break
        age = input("请输入老师年龄:")
        obj = modules.Teacher(name, age, admin)
        tearch_list.append(obj)
    if os.path.exists('db/tearch/tearch_list'):
        exists_list = pickle.load(open('db/tearch/tearch_list', 'rb'))
        tearch_list.extend(exists_list)
    pickle.dump(tearch_list, open("db/tearch/tearch_list", 'xb'))
    modules.runcode(5)


def Create_course(admin):
    course_list = []
    tearch_list = pickle.load(open('db/tearch/tearch_list', 'rb'))
    for num, item in enumerate(tearch_list, 1):
        print(num, item.Name, item.Age, item.Create_Admin.Username, item.Create_Time)
    while True:
        name = input("请输入课程名:")
        if name == 'q':
            break
        cost = input("请输入课时费:")
        tearch = input("请选择老师:")
        course_obj = modules.Course(name, cost, tearch_list[int(tearch) - 1], admin)
        course_list.append(course_obj)
        if os.path.exists('db/course/course_list'):
            exists_list = pickle.load(open('db/course/course_list', 'rb'))
            course_list.extend(exists_list)
        pickle.dump(course_list, open('db/course/course_list', 'wb'))
        modules.runcode(6)


def Login(username, passwd):
    if os.path.exists('db/admin/' + username):
        Admin_user = pickle.load(open('db/admin/' + username, 'rb'))
        if Admin_user.login(username, passwd):
            modules.runcode(0)
            while True:
                inp = input("1.创建老师\n2.创建课程\n>>>>>>>")
                if inp == '1':
                    Create_tearch(Admin_user)
                elif inp == '2':
                    Create_course(Admin_user)
        else:
            return 3
    else:
        return 1


def register(username, passwd):
    if os.path.exists('db/admin/' + username):
        return 2
    else:
        Admin_user = modules.Admin()
        r = Admin_user.register(username, passwd)
        modules.runcode(r)


def main():
    while True:
        inp = input("请输入选项:\n1.管理员登陆\n2.管理员注册\n>>>>>> ")
        username = input("请输入用户:").strip()
        passwd = input("请输入密码:")
        if inp == '1':
            r = Login(username, passwd)
            modules.runcode(r)
        elif inp == '2':
            r = register(username, passwd)
            modules.runcode(r)


if __name__ == '__main__':
    main()
