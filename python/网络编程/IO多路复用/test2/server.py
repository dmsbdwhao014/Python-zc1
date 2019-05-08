#!/usr/bin/env python
# -*- coding:utf-8 -*-

import select
import socket

IP_List = ('127.0.0.1', 9001,)

sk1 = socket.socket()
sk1.bind(IP_List)
sk1.listen()

inputs = [sk1, ]

while True:
    r_list, w_list, e_list = select.select(inputs, [], [], 1)
    print("正在监听的连接%s" % len(inputs))
    print(inputs)
    # 循环监听列表
    for sk1_or_conn in r_list:
        # 如果是新用户就添加到列表
        if sk1_or_conn == sk1:
            conn, addr = sk1_or_conn.accept()
            inputs.append(conn)
        # 如果是老用户就发送消息
        else:
            try:
                data_byte = sk1_or_conn.recv(1024)
            except Exception as ex:
                inputs.remove(sk1_or_conn)
            else:
                data_str = str(data_byte, encoding='utf-8')
                sk1_or_conn.sendall(bytes(data_str + " hello", encoding='utf-8'))
