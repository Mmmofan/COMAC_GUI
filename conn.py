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
from json import dumps
from UDP_conn import udp_receive
import tkinter as tk
from tkinter import ttk
import socket
from threading import Thread
from requests import post as req_post

class Conn(object):
    def __init__(self, root):
        self.master = root
        self.master.title('Connection')
        self.master.geometry('500x400')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')

        # 三轴
        self.server = 'http://192.168.7.254'
        self.platform_move = '/v1/mobile_platform_move'
        self.platform_send = '/v1/mobile_platform_send'
        self.token = 'NWQ7TKPAX8HC2cJDdfKFYH4kTbXAaSh4WNde4YBPSbXR5fRPji7C5hnbSD8HcpM23ABQMkKACdWrEFMkE3mfS3kFRPJYKKbzi36e2RtPyBMTCbJaRDGbCBWrX3i7FFrb'

        self.addr_val_tcp = tk.StringVar()
        self.addr_val_tcp.set("192.168.7.253")
        self.port_val_tcp= tk.IntVar()
        self.port_val_tcp.set(6000)

        self.addr_val_udp= tk.StringVar()
        self.addr_val_udp.set("127.0.0.1")
        self.port_val_udp= tk.IntVar()
        self.port_val_udp.set(10000)

        self.number_of_box = tk.IntVar()
        self.number_of_box.set(3)

        self.label_tcp = tk.Label(self.master, text='TCP', width='8', bg='yellow').place(x=20, y=70)
        self.label_udp = tk.Label(self.master, text='UDP', width='8', bg='yellow').place(x=20, y=120)
        self.label_tcp_addr = tk.Label(self.master, text='Address', width='6', bg='white').place(x=90, y=70)
        self.label_udp_addr = tk.Label(self.master, text='Address', width='6', bg='white').place(x=90, y=120)
        self.tcp_addr_box = tk.Entry(self.master, width=14, textvariable=self.addr_val_tcp).place(x=150,y=70)
        self.tcp_port_box = tk.Entry(self.master, width=6, textvariable=self.port_val_tcp).place(x=260, y=70)
        self.udp_addr_box = tk.Entry(self.master, width=14, textvariable=self.addr_val_udp).place(x=150, y=120)
        self.udp_port_box = tk.Entry(self.master, width=6, textvariable=self.port_val_udp).place(x=260, y=120)
        self.box_number_ent = tk.Entry(self.master, width=4, textvariable=self.number_of_box).place(x=320, y=120)

        self.tcp_conn = ttk.Button(self.master, width=19, text='Connect', command=self.tcp_connect)
        self.tcp_conn.place(x=320, y=68)

        self.udp_get_info = ttk.Button(self.master, width=12, text='Get Coord', command=self.udp_receive)
        self.udp_get_info.place(x=370, y=116)

        self.poseAlignment = ttk.Button(self.master, width=15, text='Pose Alignment', command=self.pose_alignment)
        self.poseAlignment.place(x=40, y=180)

    def pose_alignment(self):
        # 打开3个AGV位姿和机翼当前位姿的信息
        with open('data'+os.sep+'result.txt', 'r') as f:
            pose = f.readlines()
        AGV_pose = pose[0].strip('\n')
        wing_pose = pose[1].strip('\n')
        AGV_pose = AGV_pose.split('&')
        wing_pose = wing_pose.split('&')
        '''
        得到四个数组，分别为3个AGV和机翼的当前位姿[x, y, z, a, b, c]
        R1 - R3: 三个AGV在全局坐标系下的位姿
        W：机翼在全局坐标系下的位姿
        '''
        R1 = AGV_pose[0].split(':')
        R1 = [float(x) for x in R1[1:]] # [x, y, z, a, b, c]
        R2 = AGV_pose[1].split(':')
        R2 = [float(x) for x in R2[1:]] # [x, y, z, a, b, c]
        R3 = AGV_pose[2].split(':')
        R3 = [float(x) for x in R3[1:]] # [x, y, z, a, b, c]
        W = wing_pose[3].split(':')
        W  = [float(x) for x in W[1:]] # [x, y, z, a, b, c]
        # 当前输入位姿
        w_x, w_y, w_z, w_a, w_b, w_c = W[0], W[1], W[2], W[3], W[4], W[5]
        # 目标输入姿态
        o_a, o_b, o_c = -177.1303, 90, -87.1303  # 旋转角度
        # 球头在机翼局部坐标系下的坐标
        p1_local = [-1232.89, 986.31, -369.90]
        p2_local = [-1140.64, 2479.64, -249.89]
        p3_local = [-1940.14, 3979.78, -132.91]
        # 3个球头间的距离
        dist_12 = None
        dist_13 = None
        dist_23 = None
        # 计算球头当前在全局坐标系下坐标
        p1 = self.get_overall_coord(w_a, w_b, w_c, p1_local, [w_x, w_y, w_z])
        p2 = self.get_overall_coord(w_a, w_b, w_c, p2_local, [w_x, w_y, w_z])
        p3 = self.get_overall_coord(w_a, w_b, w_c, p3_local, [w_x, w_y, w_z])

        T = 10. # 调姿时间
        n = 100 # 划分段落

        # 读取当前三轴的情况
        coordinator1 = req_post(self.server + self.platform_move, json={"id": 1, "token": self.token}).json()['data']
        coordinator2 = req_post(self.server + self.platform_move, json={"id": 2, "token": self.token}).json()['data']
        coordinator3 = req_post(self.server + self.platform_move, json={"id": 3, "token": self.token}).json()['data']

        for k in range(n):
            # 每步转动到的角度
            delta_alpha = self.pos_track(o_a, w_a, T/n*k, T)
            delta_beta  = self.pos_track(o_b, w_b, T/n*k, T)
            delta_gamma = self.pos_track(o_c, w_c, T/n*k, T)
            # 计算球头在全局下的坐标, [x, y, z]
            p1_t = self.get_overall_coord(delta_alpha, delta_beta, delta_gamma, p1_local)
            p2_t = self.get_overall_coord(delta_alpha, delta_beta, delta_gamma, p2_local)
            p3_t = self.get_overall_coord(delta_alpha, delta_beta, delta_gamma, p3_local)
            # 计算球头在全局坐标系下的移动量, [x, y, z]
            dist1 = [(p1_t[i] - p1[i]) for i in range(3)]
            dist2 = [(p2_t[i] - p2[i]) for i in range(3)]
            dist3 = [(p3_t[i] - p3[i]) for i in range(3)]
            # 计算球头在其局部坐标系下的移动量
            dist1_trans = self.rotation_matrix(dist1, R1[3], R1[4], R1[5])
            dist2_trans = self.rotation_matrix(dist2, R2[3], R2[4], R2[5])
            dist3_trans = self.rotation_matrix(dist3, R3[3], R3[4], R3[5])

            T1 = Thread(target=self.platform_send, args=(1, T/n*1000, dist1_trans[0], dist1_trans[1], dist1_trans[2]))
            T2 = Thread(target=self.platform_send, args=(2, T/n*1000, dist2_trans[0], dist2_trans[1], dist2_trans[2]))
            T3 = Thread(target=self.platform_send, args=(3, T/n*1000, dist3_trans[0], dist3_trans[1], dist3_trans[2]))
            T1.start()
            T2.start()
            T3.start()

            del T1, T2, T3

    def rotation_matrix(self, pi, alpha, beta, gamma):
        '''
        pi: [xi, yi, zi]
        '''
        pi = np.array(pi).T
        R_x = np.array([[1, 0, 0], 
                        [0, np.cos(gamma), -np.sin(gamma)],
                        [0, np.sin(gamma), np.cos(gamma)]])
        R_y = np.array([[np.cos(beta), 0, np.sin(beta)],
                        [0, 1, 0],
                        [-np.sin(beta), 0, np.cos(beta)]])
        R_z = np.array([[np.cos(alpha), -np.sin(alpha), 0],
                        [np.sin(alpha), np.cos(alpha), 0],
                        [0, 0, 1]])
        R_phi = np.dot(np.dot(R_z, R_y), R_x)  ## 根据选择顺序决定
        res = np.dot(R_phi, pi)
        return res

    def platform_send(self, id_, t, x, y, z):
        """
        发送三轴移动量，xyz为相对移动距离
        """
        coords = req_post(self.server + self.platform_move, json={'id': id_, 'token': self.token}).json()['data']
        x_t = coords['x'] + x
        y_t = coords['y'] + y
        z_t = coords['z'] + z
        job = req_post(self.server + self.platform_send, json={'id': id_, 'token': self.token,
                                                                't':t, 'x':x_t, 'y':y_t, 'z':z_t})


    def pos_track(self, Lt, L0, t, T=10.0):
        """
        五次多项式的位置轨迹，(x, y, z, alpha, beta, gamma)
        Args:
            Lt: 目标值
            L0: 初始值
            t:  时间变量
            T:  调姿时间，常数
        """
        #Lt = np.pi / (180 / Lt) if Lt != 0 else 0
        #L0 = np.pi / (180 / L0) if L0 != 0 else 0
        res = (6*(Lt - L0)/T**5) * (t**5) + (-15*(Lt - L0)/T**4) * (t**4) + (10*(Lt - L0)/T**3) * (t**3) + L0
        return res

    def get_overall_coord(self, alpha, beta, gamma, local_coord, overall_local_diff):
        """
        已知局部坐标系和全局坐标系的差值，以及球头在局部坐标系下的坐标
        计算(三个)球头在全局坐标系下的坐标
        Args:
            alpha: 局部坐标系关于全局坐标系Z轴的转角
            beta: 局部坐标系关于全局坐标系Y轴的转角
            gamma: 局部坐标系关于全局坐标系X轴的转角
            local_coord: 球头中心在局部坐标系下坐标，在实际模型中测量
            overall_local_diff: 局部坐标系和全局坐标系（目标位置）的差值，实时数据
        """
        ### 将角度转化为弧度
        alpha = np.pi / (180 / alpha) if alpha != 0 else 0
        beta = np.pi / (180 / beta) if beta != 0 else 0
        gamma = np.pi / (180 / gamma) if gamma != 0 else 0

        R_x = np.array([[1, 0, 0], 
                        [0, np.cos(gamma), -np.sin(gamma)],
                        [0, np.sin(gamma), np.cos(gamma)]])
        R_y = np.array([[np.cos(beta), 0, np.sin(beta)],
                        [0, 1, 0],
                        [-np.sin(beta), 0, np.cos(beta)]])
        R_z = np.array([[np.cos(alpha), -np.sin(alpha), 0],
                        [np.sin(alpha), np.cos(alpha), 0],
                        [0, 0, 1]])
        R_phi = np.dot(np.dot(R_z, R_y), R_x)  ## 根据选择顺序决定

        p_n = np.array(local_coord).reshape(3, 1)
        p_m_n = np.array([overall_local_diff]).reshape(3, 1)

        P_m_i = np.dot(R_phi, p_n) + p_m_n  ## 球头中心在全局坐标系下坐标
        return P_m_i

    def udp_receive(self):
        """
        读取每个AGV的三组坐标值，并写入txt
        0 -> a, 1 -> b, 2 -> c
        """
        addr = self.addr_val_udp.get()
        port = self.port_val_udp.get()
        number = self.number_of_box.get()
        (coords, box_id) = udp_receive(addr, int(port), number) # 返回两个列表，每个列表表示n个盒子
        res_seq = ""  # AGV数据写入文件
        names = ['a', 'b', 'c']
        # 机翼标定测量值，即机翼标定点在机翼坐标系下坐标
        stand_wing_coord = {'a':[-220.21, 446.23, 15.58], 'b':[-939.23, 2360.22, 39.42], 'c':[-1258.74, 3038.71, 106.11]}

        for id_ in range(1, int(number)+1):
            local_coord = req_post(self.server + self.platform_move, json={'id': id_, 'token': self.token})
            # 三轴当前数据
            local_coord = local_coord.json()['data']
            # AGV标定测量值
            stand_agv_coord = {'a':[78.057052, -0.20528, -531.126239 - local_coord['z']],
                               'b':[-1.241144, 413.948188 + local_coord['y'], -811.497396 - local_coord['z']],
                               'c':[419.943418 + local_coord['x'], -9.058583 + local_coord['y'], -903.539647 - local_coord['z']]}
            for idx in range(len(names)):
                name = names[idx]
                res_seq += 'R{}{}:'.format(id_, name)
                res_seq += str(stand_agv_coord[name][0]) +':' # 单位mm
                res_seq += str(stand_agv_coord[name][1]) +':'
                res_seq += str(stand_agv_coord[name][2]) +':'
                res_seq += str(coords[id_-1][str(idx+1)]['X']) + ':'
                res_seq += str(coords[id_-1][str(idx+1)]['Y']) + ':'
                res_seq += str(coords[id_-1][str(idx+1)]['Z']) + '&'

        '''
        wing_res = "" # 机翼坐标写入数据
        for idx in range(1, 4):
            wing_res += 'W'+ names[idx-1] + ':'
            wing_res += str(stand_wing_coord[names[idx-1]][0]) + ':'
            wing_res += str(stand_wing_coord[names[idx-1]][1]) + ':'
            wing_res += str(stand_wing_coord[names[idx-1]][2]) + ':'
            wing_res += str(coords[-1][str(idx)]['X']) + ':'
            wing_res += str(coords[-1][str(idx)]['Y']) + ':'
            wing_res += str(coords[-1][str(idx)]['Z'])
            wing_res += '&'
        '''

        with open('data'+os.sep+'coord.txt', 'w') as f:
            f.write('1\n')
            f.write(res_seq)
            # f.write(wing_res)
        print("write coord")

    def tcp_connect(self):
        addr_tcp = self.addr_val_tcp.get()
        port = self.port_val_tcp.get()
        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_s.bind((addr_tcp, int(port)))
        self.tcp_s.listen(5)

        def tcplink(conn, addr):
            # print("Accept new connection from {}".format(addr))
            conn.send("Connection created...\n".encode('utf-8'))
            try:
                while True:
                    with open('data'+os.sep+'coord.txt', 'r') as f:
                        # data = f.readlines()
                        data = [x.strip('\n') for x in f.readlines()]
                    # data = [x.strip('\n') for x in data]
                    client = conn.recv(8192).decode('utf-8')
                    # 没有读取数据，0发0收
                    if client == "0" and data[0]=="0":
                        conn.send("0".encode('utf-8'))
                        continue
                    # 读取数据之后，发送坐标解算
                    elif client == "0" and data[0] == "1":
                        conn.send(data[1].encode('utf-8'))
                        self.AGV_Rt_str = conn.recv(8192).decode('utf-8')
                        data.append(compute_local_coord(self.AGV_Rt_str))
                        conn.send(data[2].encode('utf-8'))
                        self.wing_Rt_str = conn.recv(8192).decode('utf-8')
                        # 重新改为0，不测量
                        with open('data'+os.sep+'coord.txt', 'r+') as f:
                            f.write("0")
                        # 把收到的位姿信息解析，写入文件
                        self.parse_Rt(self.AGV_Rt_str, self.wing_Rt_str)
                        conn.send("0".encode('utf-8'))
                        continue
                    elif client == "1":
                        conn.send("1".encode('utf-8'))
            except:
                self.tcp_s.close()
                self.addr_val_tcp.set("close connection")

        conn, addr = self.tcp_s.accept()
        t = Thread(target=tcplink, args=(conn, addr))
        t.start()

    def compute_local_coord(self, agvs):
        """
        通过三个AGV的位姿信息，求解机翼当前坐标值
        agvs: {R1: {x:..., y:..., z:...}, R2: {...}, ...}
        """
        # 机翼标定测量值，即机翼球窝在机翼坐标系下坐标
        stand_wing_coord = {'a':[-1232.89, 986.31, -369.90], 'b':[-1140.64, 2479.64, -249.89], 'c':[-1940.14, 3979.78, -132.91]}
        names = ['a', 'b', 'c']
        W_str = ""
        for i in range(3):
            W_str += "W" + names[i] + ":"
            W_str += str(stand_wing_coord[names[i]][0]) + ":" # local X
            W_str += str(stand_wing_coord[names[i]][1]) + ":" # local y
            W_str += str(stand_wing_coord[names[i]][2]) + ":" # local Z
            W_str += agvs['R{}'.format(i+1)]['x'] + ":" # overall X
            W_str += agvs['R{}'.format(i+1)]['y'] + ":" # overall Y
            W_str += agvs['R{}'.format(i+1)]['z'] + "&" # overall Z

        return W_str


    def parse_Rt(self, AGV, wing):
        """
        解析AGV和机翼的位姿，以Json格式写入Poses.txt
        """
        with open('data'+os.sep+'result.txt', 'w') as f:
            f.write(AGV+'\n')
            f.write(wing)
        AGV = AGV.split('&')[:-1]
        R1 = AGV[0].split(':')
        R2 = AGV[1].split(':')
        R3 = AGV[2].split(':')
        wing = wing.split('&')[:-1]
        W = wing[0].split(':')
        R_str = {R1[0]: {"x":R1[1], "y":R1[2], "z":R1[3], "a":R1[4], "b":R1[5], "c":R1[6]},
                 R2[0]: {"x":R2[1], "y":R2[2], "z":R2[3], "a":R2[4], "b":R2[5], "c":R2[6]},
                 R3[0]: {"x":R3[1], "y":R3[2], "z":R3[3], "a":R3[4], "b":R3[5], "c":R3[6]},
                 W[0]: {"x":W[1], "y":W[2], "z":W[3], "a":W[4], "b":W[5], "c":W[6]}
                 }
        result = dumps(R_str)
        with open('data'+os.sep+'Poses.txt', 'w') as f:
            f.write(result)


if __name__ == "__main__":
    root = tk.Tk()
    master = Conn(root)
    master.master.mainloop()
