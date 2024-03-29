#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket


def handle_request(client):
    buf = client.recv(1024)
    client.sendall(bytes("HTTP/1.1 200 OK\r\n\r\n", encoding='utf-8'))
    client.sendall(bytes("Hello, World", encoding='utf-8'))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8080))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()


if __name__ == '__main__':
    main()
