#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket

ip_list = ('127.0.0.1', 9999,)

sk = socket.socket()
sk.connect(ip_list)
# recv等待发送数据阻塞
ret = str(sk.recv(1024), encoding='utf-8')
print(ret)
while True:
    inp = input("请输入发送的内容:")
    if inp == "q":
        sk.sendall(bytes(inp, encoding='utf-8'))
        print("退出")
        break
    else:
        sk.sendall(bytes(inp, encoding='utf-8'))
        ret = str(sk.recv(1024), encoding='utf-8')
        print(ret)
sk.close()
