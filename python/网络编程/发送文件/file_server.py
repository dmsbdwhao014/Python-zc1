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
    conn.sendall(bytes("欢迎登陆", encoding='utf-8'))
    file_size = int(str(conn.recv(1024), encoding='utf-8'))
    conn.sendall(bytes("ack", encoding='utf-8'))
    has_recv = 0
    f = open('new.png', 'wb')
    while True:
        if file_size == has_recv:
            break
        data = conn.recv(1024)
        f.write(data)
        has_recv += len(data)
    f.close()
