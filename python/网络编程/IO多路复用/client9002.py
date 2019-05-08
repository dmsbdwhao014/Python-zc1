#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket

IP_LIST1 = ("127.0.0.1", 9001,)
IP_LIST2 = ("127.0.0.1", 9002,)
IP_LIST3 = ("127.0.0.1", 9003,)

sk1 = socket.socket()
sk1.connect(IP_LIST2)

print(str(sk1.recv(1024), encoding='utf-8'))
sk1.close()
