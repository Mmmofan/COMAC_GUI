#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : conn.py
#   Author      : Mmmofan
#   Created date: 2019-08-31 09:36:37
#   Description :
#
#================================================================

import os
from UDP_conn import UDP_Receiver
import tkinter as tk
from tkinter import ttk
import socket
from threading import Thread

class Conn(object):
    def __init__(self, root):
        self.master = root
        self.master.title('Connection')
        self.master.geometry('500x400')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')

        self.addr_val_tcp = tk.StringVar()
        self.addr_val_tcp.set("127.0.0.1")
        self.port_val_tcp= tk.StringVar()
        self.port_val_tcp.set(6000)

        self.addr_val_udp= tk.StringVar()
        self.addr_val_udp.set("127.0.0.1")
        self.port_val_udp= tk.StringVar()
        self.port_val_udp.set(10000)

        self.label_tcp = tk.Label(self.master, text='TCP', width='8', bg='yellow').place(x=20, y=20)
        self.label_udp = tk.Label(self.master, text='UDP', width='8', bg='yellow').place(x=20, y=50)
        self.tcp_addr_box = tk.Entry(self.master, width=20, textvariable=self.addr_val_tcp).place(x=100,y=20)
        self.tcp_port_box = tk.Entry(self.master, width=8, textvariable=self.port_val_tcp).place(x=270,y=20)
        self.udp_addr_box = tk.Entry(self.master, width=20, textvariable=self.addr_val_udp).place(x=100,y=50)
        self.udp_port_box = tk.Entry(self.master, width=8, textvariable=self.port_val_udp).place(x=270,y=50)

        self.tcp_conn = ttk.Button(self.master, width=8, text='Connect', command=self.tcp_connect)
        self.tcp_conn.place(x=350, y=20)

        self.udp_get_info = ttk.Button(self.master, width=8, text='Get Coord', command=self.udp_receive)
        self.udp_get_info.place(x=350, y=50)

    def udp_receive(self):
        addr = self.addr_val_udp.get()
        port = self.port_val_udp.get()
        (coords, box_id) = UDP_Receiver(addr, int(port))
        coords_1 = coords["1"]
        coords_2 = coords["2"]
        coords_3 = coords["3"]


    def tcp_connect(self):
        addr_tcp = self.addr_val_tcp.get()
        port = self.port_val_tcp.get()
        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_s.bind((addr_tcp, int(port)))
        self.tcp_s.listen(5)

        def tcplink(conn, addr):
            conn.send("Connection created...\n".encode('utf-8'))
            with open('coord.txt', 'r') as f:
                data = f.readlines()
            data = [x.strip('\n') for x in data]
            while True:
                client = conn.recv(1024).decode('utf-8')
                print(client)
                if data[0] == '0':
                    conn.send("0".encode('utf-8'))
                    client = conn.recv(1024).decode('utf-8')
                    print(client)
                    continue
                elif data[0] == '1':
                    conn.send(data[1].encode('utf-8'))
                    client = conn.recv(1024).decode('utf-8')
                    print(client)
                    self.R_t = client
                with open('coord.txt', 'r') as f:
                    data = f.readlines()
                data = [x.strip('\n') for x in data]
        conn, addr = self.tcp_s.accept()
        t = Thread(target=tcplink, args=(conn, addr))
        t.start()


if __name__ == "__main__":
    root = tk.Tk()
    master = Conn(root)
    master.master.mainloop()
