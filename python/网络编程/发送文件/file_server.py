#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket

ip_list = ('127.0.0.1', 9999,)

sk = socket.socket()
# 绑定地址与端口
sk.bind(ip_list)
# 队列接受5个请求等待
sk.listen(5)
# 接收客户端的请求
while True:
    conn, addr = sk.accept()
    print(addr, conn)
