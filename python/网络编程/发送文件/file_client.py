# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import socket

ip_list = ('127.0.0.1', 9999,)

sk = socket.socket()
sk.connect(ip_list)

# recv阻塞等待接收数据
ret = str(sk.recv(1024), encoding='utf-8')
print(ret)

sk.recv(1024)
# 发送文件大小
file_size = os.stat('d4.png').st_size
sk.sendall(bytes(str(file_size), encoding='utf-8'))

with open('d4.png', 'rb')  as f:
    for line in f:
        sk.sendall(line)

sk.close()
