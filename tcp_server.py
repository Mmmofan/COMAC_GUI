#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading

def tcplink(conn, addr):
    print("Accept new connection from %s:%s" % addr)
    conn.send(b"Welcome!\n")
    try:
        while True:
            conn.send(b"What's your name?")
            data = conn.recv(1024)
            if data == b"exit":
                conn.send(b"Good bye!\n")
                break
            conn.send(b"Hello %s!\n" % data)
    except:
        conn.close()
    print("Connection from %s:%s is closed" % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 6000))
s.listen(5)
print("Waiting for connection...")

while True:
    conn, addr = s.accept()
    t = threading.Thread(target = tcplink, args = (conn, addr))
    t.start()