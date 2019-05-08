#!/usr/bin/env python
# -*- coding:utf-8 -*-
import select
import socket

IP_LIST1 = ("127.0.0.1", 9001,)
IP_LIST2 = ("127.0.0.1", 9002,)
IP_LIST3 = ("127.0.0.1", 9003,)

sk1 = socket.socket()
sk1.bind(IP_LIST1)
sk1.listen()

# sk2 = socket.socket()
# sk2.bind(IP_LIST2)
# sk2.listen()
#
# sk3 = socket.socket()
# sk3.bind(IP_LIST3)
# sk3.listen()

inputs = [sk1, ]

while True:
    # select.select 自动监控inputs元组的文件描述符
    r_list, w_list, e_list = select.select(inputs, [], [], 1)
    for sk in r_list:
        conn, addr = sk.accept()
        conn.sendall(bytes("hello", encoding='utf-8'))
        print(conn)
        # conn.close
