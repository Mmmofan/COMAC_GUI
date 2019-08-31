# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from control import Controller
import requests as req
import time
from threading import Thread


class Test(object):
    def __init__(self, root, server, token, id_group):
        # 定义主窗口
        self.master = root
        self.master.title('Test')
        self.master.geometry('1000x600')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')

        self.warn = False

        # 选择调试AGV
        self.choose_label = tk.Label(self.master, text='选择调试AGV', bg='yellow', font=('Arial', 12), width=16).place(x=40,y=30)
        self.id_group = id_group
        self.agv_var = tk.StringVar()
        r1 = tk.Radiobutton(self.master, text='AGV 1', bg='white', variable=self.agv_var, value='1', command=self.set_id)
        r2 = tk.Radiobutton(self.master, text='AGV 2', bg='white', variable=self.agv_var, value='2', command=self.set_id)
        r3 = tk.Radiobutton(self.master, text='AGV 3', bg='white', variable=self.agv_var, value='3', command=self.set_id)
        r1.place(x=180, y=30)
        r2.place(x=270, y=30)
        r3.place(x=360, y=30)

        # 定义私有变量
        self.server = server
        self.token = token
        self.vel                      = '/v1/cmd_vel'
        self.jack_up_down             = '/v1/jack_up'
        self.follow                   = '/v1/follow'
        self.mobile_platform_move     = '/v1/mobile_platform_move'
        self.mobile_platform_send     = '/v1/mobile_platform_send'
        self.mobile_platform_pressure = '/v1/mobile_platform_pressure'
        self.moving = None

        # 定义组件
        ## 平台不动，AGV转向，输入弧度
        ## 按钮
        self.button_1 = ttk.Button(self.master, text='Follow', width='16', command=self.func_1)
        self.button_1.place(x=70, y=120)
        ## 转向弧度输入
        self.follow_angle_var = tk.StringVar()
        self.follow_angle_var.set('0.1')
        self.follow_angle = tk.Entry(self.master,width=10, font=('Arial', 10), textvariable=self.follow_angle_var)
        self.follow_angle.place(x=200,y=120)
        self.follow_label = tk.Label(self.master, text='返回值：', bg='white', font=('Arial', 10), width=6).place(x=285,y=120)
        ## 返回值
        self.return_follow = tk.StringVar()
        self.return_follow.set("接收返回值")
        self.return_box_1 = tk.Entry(self.master, width=25, font=('Arial', 10), textvariable=self.return_follow).place(x=350,y=120)

        # 直线运动，或转向，输入速度或角速度
        ## 按钮
        self.button_2 = ttk.Button(self.master, text='Move / Rotate', width='16', command=self.func_2)
        self.button_2.place(x=70, y=235)
        ## 速度，角速度设置
        self.mr_speed = tk.StringVar()
        self.mr_speed.set("0.0")
        self.mr_angle = tk.StringVar()
        self.mr_angle.set("0.0")
        self.mr_m = tk.Entry(self.master,width=10, font=('Arial', 10), textvariable=self.mr_speed).place(x=300,y=220)
        self.mr_r = tk.Entry(self.master, width=10, font=('Arial', 10), textvariable=self.mr_angle).place(x=300,y=250)
        self.vel_label = tk.Label(self.master, text='运动速度：', bg='white', font=('Arial', 10), width=10).place(x=200,y=220)
        self.rot_label = tk.Label(self.master, text='旋转弧度：', bg='white', font=('Arial', 10), width=10).place(x=200,y=250)

        # 读取力传感器数值
        self.force_label = tk.Label(self.master, text='受力情况', bg='white', font=('Arial', 10), width=6).place(x=485,y=250)
        self.read_sensor_bt = ttk.Button(self.master, text='Get Sensor', width='16', command=self.read_sensor)
        self.read_sensor_bt.place(x=485, y=220)
        self.cur_pressure = tk.StringVar()
        self.cur_pressure.set("接收返回值")
        self.cur_pressure_en = tk.Entry(self.master, width=35, font=('Arial', 10), textvariable=self.cur_pressure).place(x=550,y=250)

        # 输入坐标值，调试三轴平台
        ## 调试按钮
        self.button_3 = ttk.Button(self.master, text='Coordinator', width='16', command=self.func_3)
        self.button_3.place(x=70, y=360)
        self.t_platform_label = tk.Label(self.master, text='运行时间: ', bg='white', font=('Arial', 10), width=10).place(x=200,y=425)
        self.x_platform_label = tk.Label(self.master, text='X轴坐标：', bg='white', font=('Arial', 10), width=10).place(x=200,y=335)
        self.y_platform_label = tk.Label(self.master, text='y轴坐标：', bg='white', font=('Arial', 10), width=10).place(x=200,y=365)
        self.z_platform_label = tk.Label(self.master, text='z轴坐标：', bg='white', font=('Arial', 10), width=10).place(x=200,y=395)
        ## 数值
        self.x_coord = tk.StringVar()
        self.x_coord.set("0.0")
        self.y_coord = tk.StringVar()
        self.y_coord.set("0.0")
        self.z_coord = tk.StringVar()
        self.z_coord.set("0.0")
        self.t_num = tk.StringVar()
        self.t_num.set("2000")
        self.x_coord_ent = tk.Entry(self.master,width=10, font=('Arial', 10), textvariable=self.x_coord).place(x=300,y=335)
        self.y_coord_ent = tk.Entry(self.master, width=10, font=('Arial', 10), textvariable=self.y_coord).place(x=300,y=365)
        self.z_coord_ent = tk.Entry(self.master, width=10, font=('Arial', 10), textvariable=self.z_coord).place(x=300,y=395)
        self.t_num_ent = tk.Entry(self.master, width=10, font=('Arial', 10), textvariable=self.t_num).place(x=300, y=425)

        # 读取三轴平台坐标值
        self.cur_coord_label = tk.Label(self.master, text='当前坐标', bg='white', font=('Arial', 10), width=6).place(x=485,y=360)
        self.cur_coord = tk.StringVar()
        self.cur_coord.set("接收返回值")
        self.cur_coord_en = tk.Entry(self.master, width=35, font=('Arial', 10), textvariable=self.cur_coord).place(x=550,y=360)
        self.read_coord_bt = ttk.Button(self.master, text='Get Coord', width='16', command=self.read_coord)
        self.read_coord_bt.place(x=485, y=330)

        # Test 1: 车动，并实时读取传感器值
        self.step1_button = ttk.Button(self.master, text='Step1', width=10, command=self.step1_func)
        self.step1_button.place(x=650, y=120)

    def set_id(self):
        self.robot_id = self.id_group[self.agv_var.get()]['robot_id']
        self.id_ = self.id_group[self.agv_var.get()]['id_']


    def func_1(self):
        """
        Follow 按钮功能，三轴不动AGV旋转
        """
        follow_var = float(self.follow_angle_var.get())
        job = req.post(self.server + self.follow, json={'token' : self.token,
                                                        'follow' : follow_var,
                                                        'robot_id' : self.robot_id})
        self.return_follow.set(job.json()['data'['code']])


    def func_2(self):
        """
        AGV 移动功能
        """
        self.moving = True
        speed = float(self.mr_speed.get())
        angle = float(self.mr_angle.get())
        tmp_speed = 0
        # while not self.warn:
        #     if tmp_speed < speed and speed != 0:
        #         tmp_speed += 0.02
        for i in range(30):
            if self.warn:
                break
            job = req.post(self.server + self.vel, json={'token' : self.token,
                                                        'speed' : speed,
                                                        'angle' : angle,
                                                        'robot_id' : self.robot_id})
            time.sleep(1/20.0)
        self.moving = False


    def func_3(self):
        """
        三轴
        """
        t = float(self.t_num.get())
        x = float(self.x_coord.get())
        y = float(self.y_coord.get())
        z = float(self.z_coord.get())
        job = req.post(self.server + self.mobile_platform_send, json={'t': t,'x' : x, 'y' : y, 'z' : z,
                                                                    'id' : self.id_, 'token': self.token})


    def read_sensor(self):
        # while not self.warn and self.moving:
        job = req.post(self.server + self.mobile_platform_pressure, json={'id' : self.id_,
                                                                        'token' : self.token})
        data = job.json()['data']
        self.cur_pressure.set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))
        if abs(data['x']) > 20 or abs(data['y']) > 20:
            self.warn = True
        time.sleep(0.2)


    def read_coord(self):
        job = req.post(self.server + self.mobile_platform_move, json={'id': self.id_,
                                                                    'token': self.token})
        data = job.json()['data']
        self.cur_coord.set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))
        time.sleep(0.2)


    def step1_func(self):
        t1 = Thread(target=self.func_2)
        t2 = Thread(target=self.read_sensor)
        # t3 = Thread(name=self.read_coord)
        print('Thread create')
        t1.start()
        t2.start()
        # t3.start()
        print('Thread start')


if __name__ == "__main__":
    server = 'http://192.168.7.254'
    token = 'NWQ7TKPAX8HC2cJDdfKFYH4kTbXAaSh4WNde4YBPSbXR5fRPji7C5hnbSD8HcpM23ABQMkKACdWrEFMkE3mfS3kFRPJYKKbzi36e2RtPyBMTCbJaRDGbCBWrX3i7FFrb'
    robot_id_group = {'1' : {'robot_id':'W50020190812003', 'id_':1},
                      '2' : {'robot_id':'W50020190703001', 'id_':2},
                      '3' : {'robot_id':'W50020190812002', 'id_':3}}
    # 251 : 1
    # 252 : 2
    # 253 : 3

    test = Test(tk.Tk(), server, token, robot_id_group)
    test.master.mainloop()
