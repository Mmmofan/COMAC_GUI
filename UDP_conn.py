#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : conn.py
#   Author      : Mmmofan
#   Created date: 2019-08-30 16:17:30
#   Description :
#
#================================================================
import socket
import json

def udp_receive(addr, port, number):
    '''
    {"coord":{"3":{"Flags":0,"TransCount":"2.4.","Valid":true,"X":6457.98193359375,"Y":-3672.16162109375,"Z":-9470.173828125}},
    "id":590593573,
    "raw":{"3":{"2":{"Flags":0,"LocalCount":253343952,"RPM":1800,"T":33.340641021728516,"t1":0.9559048414230347,"t2":0.2501751780509949},
    "4":{"Flags":0,"LocalCount":254042966,"RPM":1750,"T":34.28936004638672,"t1":0.44152122735977173,"t2":0.721427321434021}}}}
    '''
    class UDP_Receiver(object):
        def __init__(self, host, port, buffsize):
            self.server_host = host
            self.server_port = port
            self.buffsize = buffsize
            self.addr = (self.server_host, self.server_port)
            self.data = []
            self.udp_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.udp_client.bind(self.addr)

        def read_data(self):
            data = self.udp_client.recv(self.buffsize)
            dict_data = json.loads(data.decode('utf-8'))
            self.data = dict_data
        
        def close(self):
            self.udp_client.close()

    udp_receiver = UDP_Receiver(addr, port, 8192) # 创建UDP的接收模块
    coords = []
    ids = []
    for i in range(number):
        udp_receiver.read_data()
        coords.append(udp_receiver.data["coord"])
        ids.append(udp_receiver.data["id"])
    udp_receiver.close()
    return coords, ids
