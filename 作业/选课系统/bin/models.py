#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pickle
import time
import os
import getpass


class Teacher:
    def __init__(self, name, age, admin):
        self.Name =  name
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
        if os.path.exists('db/' + self.Username):
            return 2
        else:
            pickle.dump(self, open('db/' + self.Username, 'xb'))
            return 4


def Login(username, passwd):
    if os.path.exists('db/'+username):
        Admin_user = pickle.load(open('db/' + username, 'rb'))
        if Admin_user.login(username, passwd):
            return 0
        else:
            return 3
    else:
        return 1


def register(username, passwd):
    if os.path.exists('db/'+username):
        return 2
    else:
        Admin_user = Admin()
        r = Admin_user.register(username, passwd)
        errorcode(r)


def errorcode(code):
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


def main():
    while True:
        inp = input("请输入选项:\n1.管理员登陆\n2.管理员注册\n>>>>>> ")
        username = input("请输入用户:").strip()
        passwd = input("请输入密码:")
        if inp == '1':
            r = Login(username, passwd)
            errorcode(r)
        elif inp == '2':
            r = register(username, passwd)
            errorcode(r)


if __name__ == '__main__':
    main()

"""
:return code 0 : login successful
:return code 1 : the user not exists
:return code 2 : the user is exists
:return code 3 : username or password is incorrect
"""
