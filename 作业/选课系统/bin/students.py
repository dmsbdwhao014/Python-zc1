#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))


def login(user, passwd):
    pass


def register(uase, passwd):
    pass


def main():
    inp = input("1.登陆\n2.注册\n>>>>>>")
    user = input("用户名:")
    passwd = input("密码:")
    if inp == '1':
        login(user, passwd)
    elif inp == '2':
        register(user, passwd)


if __name__ == '__main__':
    main()
