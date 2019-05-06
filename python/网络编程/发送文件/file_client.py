#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket

ip_list = ('127.0.0.1', 9999,)

sk = socket.socket()
sk.connect(ip_list)
# recv等待发送数据阻塞
ret = str(sk.recv(1024), encoding='utf-8')
print(ret)

sk.close()
