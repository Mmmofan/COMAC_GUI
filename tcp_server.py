#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading

def tcplink(conn, addr):
    with open('coord.txt', 'r') as f:
        coord = f.readline()
    print("Accept new connection from %s:%s" % addr)
    conn.send("Connection created...\n".encode('utf-8'))
    try:
        while True:
            conn.send(b"Waiting for message")
            data = conn.recv(1024).decode('utf-8')
            if data == "exit":
                conn.send("Exit...\n".encode('utf-8'))
                break
            elif data == "0":
                conn.send('1'.encode('utf-8'))
            elif data == "1":
                conn.send("1".encode('utf-8'))
            elif data == "2":
                conn.send("{}".format(coord).encode('utf-8'))
            elif data.startswith('R'):
                print("get data")
                conn.send("complete".encode('utf-8'))

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
