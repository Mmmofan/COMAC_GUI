#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 6000))
# print(s.recv(1024).decode())
# data = "client"

while True:
    data = s.recv(1024).decode('utf-8')
    if data == "0":
        s.send("0".encode('utf-8'))
        continue
    # data = input("Please input your name: ")
    elif data == "1":
        s.send("Start measuring".encode('utf-8'))
        continue
    elif data.startswith('R'):
        s.send("IGPS".encode('utf-8'))
        continue
    elif data == "Exit...\n":
        s.send('exit tcp')
        break
    else:
        print(data)
        new = input("which state?")
        s.send(new.encode('utf-8'))

s.close()
