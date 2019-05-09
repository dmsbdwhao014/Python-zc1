#!/usr/bin/env python
# -*- coding:utf-8 -*-

import select
import socket

IP_List = ('127.0.0.1', 9001,)

sk1 = socket.socket()
sk1.bind(IP_List)
sk1.listen()

inputs = [sk1, ]
outputs = []
message_dict = {}
while True:
    r_list, w_list, e_list = select.select(inputs, outputs, inputs, 1)
    print("正在监听的连接%s" % len(inputs))
    print(inputs)
    # 循环监听列表
    for sk1_or_conn in r_list:
        # 如果是新用户就添加到列表
        if sk1_or_conn == sk1:
            conn, addr = sk1_or_conn.accept()
            inputs.append(conn)
            message_dict[conn] = []
        # 如果是老用户就发送消息
        else:
            try:
                data_byte = sk1_or_conn.recv(1024)
            except Exception as ex:
                inputs.remove(sk1_or_conn)
            data_str = str(data_byte, encoding='utf-8')
            message_dict[sk1_or_conn].append(data_str)
            outputs.append(sk1_or_conn)

    for sk1_or_conn in w_list:
        recv_str = message_dict[conn][0]
        del message_dict[conn][0]
        sk1_or_conn.sendall(bytes(recv_str + " hello", encoding='utf-8'))
        outputs.remove(sk1_or_conn)

    for sk1_or_conn in e_list:
        inputs.remove(sk1_or_conn)
