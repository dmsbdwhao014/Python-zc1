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
    conn, addr = sk.accept()  # 等待连接阻塞
    conn.sendall(bytes("欢迎光临", encoding='utf-8'))
    while True:
        recv_byte = conn.recv(1024)
        ret_str = str(recv_byte, encoding='utf-8')
        if ret_str == 'q':
            print("退出")
            break
        conn.sendall(bytes(ret_str + '好', encoding='utf-8'))
        print(addr, conn)
