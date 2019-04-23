#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pickle
import time
import os
import getpass

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

        pickle.dump(self, open(self.Username, 'xb'))



def main():
    inp = input("请输入选项:\n1.管理员登陆\n2.管理员注册\n>>>>>> ")
    if inp == '1':
        username = input("请输入用户:").strip()
        passwd = input("请输入密码:")
        if os.path.exists(username):
            Admin_user = pickle.load(open(username, 'rb'))
            if Admin_user.login(username,passwd):
                print("登陆成功")
            else:
                print("用户名或者密码错")
        else:
            print("用户不存在")
    elif inp == '2':
        username = input("请输入用户:").strip()
        passwd = input("请输入密码:")
        if os.path.exists(username):
            print("用户已经存在")
        else:
            Admin_user = Admin()
            Admin_user.register(username,passwd)


if __name__ == '__main__':
    main()
