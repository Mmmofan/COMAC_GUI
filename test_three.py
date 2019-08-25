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
        self.master.geometry('1000x600')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')

        self.warn = False#力超过阈值报警，三车共有，一车报警，全部停
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
        self.agv1_speed=tk.StringVar()
        self.agv1_speed.set('0.0')
        self.agv1_speed_box=tk.Entry(self.master,width=16, font=('Arial', 10), textvariable=self.agv1_speed).place(x=200,y=150)
        self.agv2_speed = tk.StringVar()
        self.agv2_speed.set('0.0')
        self.agv2_speed_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv2_speed).place(
            x=400, y=150)
        self.agv3_speed = tk.StringVar()
        self.agv3_speed.set('0.0')
        self.agv3_speed_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv3_speed).place(
            x=600, y=150)

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
        self.agv1_sensor_box=tk.Entry(self.master,width=16, font=('Arial', 10), textvariable=self.agv1_sensor).place(x=200,y=250)
        self.agv2_sensor = tk.StringVar()
        self.agv2_sensor.set('力传感器返回值')
        self.agv2_sensor_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv2_sensor).place(
            x=400, y=250)
        self.agv3_sensor = tk.StringVar()
        self.agv3_sensor.set('力传感器返回值')
        self.agv3_sensor_box = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.agv3_sensor).place(
            x=600, y=250)

        self.start=tk.Button(self.master, text='START', width='16', command=self.thread_start).place(x=400,y=350)

        self.speed={1:self.agv1_speed,2:self.agv2_speed,3:self.agv3_speed}
        self.sensor={1:self.agv1_sensor,2:self.agv2_sensor,3:self.agv3_sensor}
        self.angel={1:self.agv1_angel,2:self.agv2_angel,3:self.agv3_angel}
        self.moving={1:self.moving1,2:self.moving2,3:self.moving3}

#threadlocal感觉适合几个单独级别一样的线程，现在想写个3线程，每个线程底下还有两线程，所以先没用threadlocal

    def set_id(self,id):
        #一个id输入就够了
        # robot_id = self.id_group[id]['robot_id']
        # id_= self.id_group[id]['id_']
        t1=Thread(target=self.move,args=(id,))#每个车两个线程，一个走，一个读力传感器
        t2=Thread(target=self.read_sensor,args=(id,))
        t1.start()
        t2.start()



    def thread_start(self):
        t1=Thread(target=self.set_id,args=(1,))#三条线程，都是set_id出发，设置每台车id，输入值为该车ID
        t2 = Thread(target=self.set_id,args=(2,))
        t3 = Thread(target=self.set_id,args=(3,))
        print('Thread create')
        t1.start()
        t2.start()
        t3.start()
        print('Thread start')

    def move(self,id):
        self.moving[id] = True
        speed = float(self.speed[id].get())
        angle = float(self.angel[id].get())
        tmp_speed = 0
        # while not self.warn:
        #     if tmp_speed < speed and speed != 0:
        #         tmp_speed += 0.02
        for i in range(30):#速度没设加减速，今天的加减速没push到github上，之后可以加，影响不大
            if self.warn:
                break
            job = req.post(self.server + self.vel, json={'token' : self.token,
                                                        'speed' : speed,
                                                        'angle' : angle,
                                                        'robot_id' :self.id_group[id]['robot_id']})
            time.sleep(1/20.0)
        self.moving[id] = False

    def read_sensor(self,id):
        while not self.warn and self.moving[id]:
            job = req.post(self.server + self.mobile_platform_pressure, json={'id' : id,
                                                                            'token' : self.token})
            data = job.json()['data']
            self.sensor[id].set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))
            if abs(data['x']) > 35 or abs(data['y']) > 35:
                self.warn = True
            time.sleep(0.2)


if __name__ == "__main__":
    server = 'http://192.168.7.254'
    token = 'NWQ7TKPAX8HC2cJDdfKFYH4kTbXAaSh4WNde4YBPSbXR5fRPji7C5hnbSD8HcpM23ABQMkKACdWrEFMkE3mfS3kFRPJYKKbzi36e2RtPyBMTCbJaRDGbCBWrX3i7FFrb'
    robot_id_group = {1 : {'robot_id':'W50020190812003', 'id_':1},
                      2 : {'robot_id':'W50020190703001', 'id_':2},
                      3 : {'robot_id':'W50020190812002', 'id_':3}}

    test = Test_three(tk.Tk(), server, token, robot_id_group)
    test.master.mainloop()