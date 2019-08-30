#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading

def tcplink(conn, addr):
    with open('coord.txt', 'r') as f:
        coord = f.readline()
    print("Accept new connection from %s:%s" % addr)
    conn.send(b"Connection created...\n")
    try:
        while True:
            conn.send(b"Waiting for message")
            data = conn.recv(1024)
            if data == b"exit":
                conn.send(b"Exit...\n")
                break
            elif data == b"2":
                conn.send(b"{}".format(coord))
            elif data == b"1":
                conn.send(b"1")
            elif data.startswith('R'):
                print("get data")
            conn.send(b"1")

    except:
        conn.close()
    print("Connection from %s:%s is closed" % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.7.251", 6000))
s.listen(5)
print("Waiting for connection...")

while True:
    conn, addr = s.accept()
    t = threading.Thread(target = tcplink, args = (conn, addr))
    t.start()
