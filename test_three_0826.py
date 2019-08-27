import tkinter as tk
from tkinter import ttk
import requests as req
import time
from threading import Thread
import threading

class Test_three(object):
    def __init__(self, root, server, token, id_group):
        # 定义主窗口
        self.master = root
        self.master.title('Test_three')
        self.master.geometry('1000x800')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')

        self.warn = False #力超过阈值报警，三车共有，一车报警，全部停
        self.stop_button = False
        self.id_group = id_group
        self.server = server
        self.token = token
        self.vel                      = '/v1/cmd_vel'
        self.jack_up_down             = '/v1/jack_up'
        self.follow                   = '/v1/follow'
        self.mobile_platform_move     = '/v1/mobile_platform_move'
        self.mobile_platform_send     = '/v1/mobile_platform_send'
        self.mobile_platform_pressure = '/v1/mobile_platform_pressure'
        self.moving1 = None#三个车的一个flag指标，每个车一个，这个车停了，这个指标会告诉力传感器读数停止
        self.moving2 = None
        self.moving3 = None
        self.labe11=tk.Label(self.master,text='AGV1', width='16',bg='yellow').place(x=200,y=100)
        self.labe12 = tk.Label(self.master, text='AGV2', width='16', bg='yellow').place(x=400, y=100)
        self.labe13 = tk.Label(self.master, text='AGV3', width='16', bg='yellow').place(x=600, y=100)
        self.labe21=tk.Label(self.master,text='运行速度',width='14',bg='white').place(x=50,y=150)
        self.labe22=tk.Label(self.master,text='旋转速度',width='14',bg='white').place(x=50,y=200)
        self.labe31=tk.Label(self.master,text='传感器返回值',width='14',bg='white').place(x=50,y=250)
        self.labe32 = tk.Label(self.master, text='传感器阀值', width='14', bg='white').place(x=50, y=300)
        self.agv1_speed=tk.StringVar()
        self.agv1_speed.set('0.05')
        self.agv1_speed_box=tk.Entry(self.master,width=16, font=('Arial', 10), textvariable=self.agv1_speed).place(x=200,y=150)
        self.agv2_speed = tk.StringVar()
        self.agv2_speed.set('0.05')
        self.agv2_speed_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv2_speed).place(
            x=400, y=150)
        self.agv3_speed = tk.StringVar()
        self.agv3_speed.set('0.05')
        self.agv3_speed_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv3_speed).place(
            x=600, y=150)
        self.Tourque_Limit = tk.StringVar()
        self.Tourque_Limit.set('35')
        self.Tourque_Limit_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.Tourque_Limit).place(
            x=200, y=300)

        self.agv1_angel=tk.StringVar()
        self.agv1_angel.set('0.0')
        self.agv1_angel_box=tk.Entry(self.master,width=16, font=('Arial', 10), textvariable=self.agv1_angel).place(x=200,y=200)
        self.agv2_angel = tk.StringVar()
        self.agv2_angel.set('0.0')
        self.agv2_angel_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv2_angel).place(
            x=400, y=200)
        self.agv3_angel = tk.StringVar()
        self.agv3_angel.set('0.0')
        self.agv3_angel_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv3_angel).place(
            x=600, y=200)

        self.agv1_sensor=tk.StringVar()
        self.agv1_sensor.set('力传感器返回值')
        self.agv1_sensor_box=tk.Entry(self.master,width=20, font=('Arial', 10), textvariable=self.agv1_sensor).place(x=200,y=250)
        self.agv2_sensor = tk.StringVar()
        self.agv2_sensor.set('力传感器返回值')
        self.agv2_sensor_box = tk.Entry(self.master, width=20, font=('Arial', 10), textvariable=self.agv2_sensor).place(
            x=400, y=250)
        self.agv3_sensor = tk.StringVar()
        self.agv3_sensor.set('力传感器返回值')
        self.agv3_sensor_box = tk.Entry(self.master, width=20, font=('Arial', 10), textvariable=self.agv3_sensor).place(
            x=600, y=250)

        self.start=tk.Button(self.master, text='START', width='16', command=self.thread_start).place(x=200,y=650)
        self.stop = tk.Button(self.master, text='STOP', width='16', command=self.stop_id).place(x=350, y=650)
        self.reset = tk.Button(self.master, text='RESET', width='16', command=self.rst).place(x=500, y=650)
        self.coordinator = tk.Button(self.master, text='Coordinator', width='16', command=self.move_poge_id).place(x=650, y=650)
        # 输入坐标值，调试三轴平台
        ## 调试按钮

        self.t_platform_label = tk.Label(self.master, text='运行时间: ', bg='white', font=('Arial', 10), width=14).place(
            x=50, y=350)
        self.x_platform_label = tk.Label(self.master, text='X轴坐标：', bg='white', font=('Arial', 10), width=14).place(
            x=50, y=400)
        self.y_platform_label = tk.Label(self.master, text='y轴坐标：', bg='white', font=('Arial', 10), width=14).place(
            x=50, y=450)
        self.z_platform_label = tk.Label(self.master, text='z轴坐标：', bg='white', font=('Arial', 10), width=14).place(
            x=50, y=500)
        ## 数值
        self.x1_coord = tk.StringVar()
        self.x1_coord.set("0.0")
        self.y1_coord = tk.StringVar()
        self.y1_coord.set("0.0")
        self.z1_coord = tk.StringVar()
        self.z1_coord.set("0.0")
        self.x2_coord = tk.StringVar()
        self.x2_coord.set("0.0")
        self.y2_coord = tk.StringVar()
        self.y2_coord.set("0.0")
        self.z2_coord = tk.StringVar()
        self.z2_coord.set("0.0")
        self.x3_coord = tk.StringVar()
        self.x3_coord.set("0.0")
        self.y3_coord = tk.StringVar()
        self.y3_coord.set("0.0")
        self.z3_coord = tk.StringVar()
        self.z3_coord.set("0.0")
        self.t_num = tk.StringVar()
        self.t_num.set("5000.0")
        self.x1_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.x1_coord).place(x=200,
                                                                                                                y=400)
        self.x2_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.x2_coord).place(x=400,
                                                                                                                y=400)
        self.x3_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.x3_coord).place(x=600,
                                                                                                                y=400)
        self.y1_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.y1_coord).place(x=200,
                                                                                                                y=450)
        self.y2_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.y2_coord).place(x=400,
                                                                                                                y=450)
        self.y3_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.y3_coord).place(x=600,
                                                                                                                y=450)
        self.z1_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.z1_coord).place(x=200,
                                                                                                                y=500)
        self.z2_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.z2_coord).place(x=400,
                                                                                                                y=500)
        self.z3_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.z3_coord).place(x=600,
                                                                                                                y=500)
        self.t_num_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.t_num).place(x=200,
                                                                                                            y=350)

        # 读取三轴平台坐标值
        self.cur_coord_label = tk.Label(self.master, text='当前坐标', bg='white', font=('Arial', 10), width=14).place(x=50,
                                                                                                                 y=550)
        self.cur_coord1 = tk.StringVar()
        self.cur_coord1.set("接收返回值")
        self.cur_coord1_en = tk.Entry(self.master, width=20, font=('Arial', 10), textvariable=self.cur_coord1).place(
            x=200, y=550)
        self.cur_coord2 = tk.StringVar()
        self.cur_coord2.set("接收返回值")
        self.cur_coord2_en = tk.Entry(self.master, width=20, font=('Arial', 10), textvariable=self.cur_coord2).place(
            x=400, y=550)
        self.cur_coord3 = tk.StringVar()
        self.cur_coord3.set("接收返回值")
        self.cur_coord3_en = tk.Entry(self.master, width=20, font=('Arial', 10), textvariable=self.cur_coord3).place(
            x=600, y=550)



        self.speed={1:self.agv1_speed,2:self.agv2_speed,3:self.agv3_speed}
        self.sensor={1:self.agv1_sensor,2:self.agv2_sensor,3:self.agv3_sensor}
        self.angel={1:self.agv1_angel,2:self.agv2_angel,3:self.agv3_angel}
        self.moving={1:self.moving1,2:self.moving2,3:self.moving3}
        self.cur_coord = {1: self.cur_coord1, 2: self.cur_coord2, 3: self.cur_coord3}
        self.x_coord = {1: self.x1_coord, 2: self.x2_coord, 3: self.x3_coord}
        self.y_coord = {1: self.y1_coord, 2: self.y2_coord, 3: self.y3_coord}
        self.z_coord = {1: self.z1_coord, 2: self.z2_coord, 3: self.z3_coord}

#threadlocal感觉适合几个单独级别一样的线程，现在想写个3线程，每个线程底下还有两线程，所以先没用threadlocal

    def set_id(self,id_):
        #一个id输入就够了
        # robot_id = self.id_group[id]['robot_id']
        # id_= self.id_group[id]['id_']
        t1=Thread(target=self.move,args=(id_,))#每个车两个线程，一个走，一个读力传感器
        t2=Thread(target=self.read_sensor,args=(id_,))
    #    t3=Thread(target=self.read_coord,args=(id_,))
        t1.start()
        t2.start()
    #    t3.start()


    def stop_id(self):
        self.stop_button = True

    def move_poge_id(self):
        t1=Thread(target=self.move_poge,args=(1,))
        t2=Thread(target=self.move_poge, args=(2,))
        t3=Thread(target=self.move_poge, args=(3,))
        t4 = Thread(target=self.read_coord, args=(1,))
        t5 = Thread(target=self.read_coord, args=(2,))
        t6 = Thread(target=self.read_coord, args=(3,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

    def thread_start(self):
        t1=Thread(target=self.set_id,args=(1,))#三条线程，都是set_id出发，设置每台车id，输入值为该车ID
        t2 = Thread(target=self.set_id,args=(2,))
        t3 = Thread(target=self.set_id,args=(3,))
        print('Thread create')
        t1.start()
        t2.start()
        t3.start()
        print('Thread start')

    def move(self,id_):

        self.moving[id_] = True
        speed = float(self.speed[id_].get())
        angle = float(self.angel[id_].get())
        tmp_speed = 0
        # while not self.warn:
        #     if tmp_speed < speed and speed != 0:
        #         tmp_speed += 0.02
        for i in range(100):#速度没设加减速，今天的加减速没push到github上，之后可以加，影响不大
            if self.warn or self.stop_button:
                job = req.post(self.server + self.vel, json={'token' : self.token,
                                                        'speed' : 0,
                                                        'angle' : 0,
                                                        'robot_id' :self.id_group[id_]['robot_id']})
            else:
                job = req.post(self.server + self.vel, json={'token' : self.token,
                                                        'speed' : speed,
                                                        'angle' : angle,
                                                        'robot_id' :self.id_group[id_]['robot_id']})
                time.sleep(1/20.0)
        self.moving[id_] = False

    def read_sensor(self,id_):

#        while not self.warn and self.moving[id]:#如果没报警，没停车，一直读数
        while True:  # 如果没报警，没停车，一直读数
            job = req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,
                                                                            'token' : self.token})
            data = job.json()['data']
            self.sensor[id_].set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))

            if abs(data['x']) > 35 or abs(data['y']) > 35:
                self.warn = True
            time.sleep(0.2)

    def rst(self):
        self.warn = False
        self.stop_button = False


    def move_poge(self,id_):
        t = float(self.t_num.get())
        x = float(self.x_coord[id_].get())
        y = float(self.y_coord[id_].get())
        z = float(self.z_coord[id_].get())
        job = req.post(self.server + self.mobile_platform_send, json={'t': t,'x' : x, 'y' : y, 'z' : z,
                                                                    'id' : id_, 'token': self.token})

    def read_coord(self,id_):
        while True:
            job = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                    'token': self.token})
            data = job.json()['data']
            self.cur_coord[id_].set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))

if __name__ == "__main__":
    server = 'http://192.168.7.254'
    token = 'NWQ7TKPAX8HC2cJDdfKFYH4kTbXAaSh4WNde4YBPSbXR5fRPji7C5hnbSD8HcpM23ABQMkKACdWrEFMkE3mfS3kFRPJYKKbzi36e2RtPyBMTCbJaRDGbCBWrX3i7FFrb'
    robot_id_group = {1 : {'robot_id':'W50020190812003', 'id_':1},
                      2 : {'robot_id':'W50020190703001', 'id_':2},
                      3 : {'robot_id':'W50020190812002', 'id_':3}}

    test = Test_three(tk.Tk(), server, token, robot_id_group)
 #   test.read_coord_id()
    test.master.mainloop()