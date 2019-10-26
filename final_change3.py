import copy
import math
import time
import tkinter as tk
from math import pi
from threading import Thread

import matplotlib.pyplot as plt
import numpy as np
import requests as req

from fuzzy_controller import fuzzy_controller


class three_all_change(object):
    def __init__(self, root, server, token, id_group, zfirst=0., xcar=0., ycar=0., xcord=0., ycord=0., zcord=0.,
        nxcord=0., nycord=0., nzcord=0., nxcar=0., nycar=0., nzfirst=0.):
        # 定义主窗口
        self.end = False
        self.master = root
        self.nxcar = nxcar
        self.nycar = nycar
        self.nzfirst = nzfirst
        self.nxcord = nxcord
        self.nycord = nycord
        self.nzcord = nzcord
        self.xcar = xcar
        self.ycar = ycar
        self.xcord = xcord
        self.ycord = ycord
        self.zcord = zcord
        self.zfirst = zfirst
        self.flag = 1
        self.stop = 0
        self.master.title('COMAC')
        self.plot_flag=False
        self.master.geometry('1080x960')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')
        self.fuzzy_controller_x=fuzzy_controller(np.arange(-20,20.5,0.5),np.arange(-20,20.5,0.5),np.arange(-5,5.5,0.5),np.arange(-1,1.1,0.1),np.arange(-5,5.5,0.5),'fx',
                                                 'dfx',['nb','nm','ns','z','ps','pm','pb'])
        self.fuzzy_controller_y=fuzzy_controller(np.arange(-20,20.5,0.5),np.arange(-20,20.5,0.5),np.arange(-5,5.5,0.5),np.arange(-1,1.1,0.1),np.arange(-5,5.5,0.5),'fy',
                                                 'dfy',['nb','nm','ns','z','ps','pm','pb'])
        # self.x,self.y,self.z=0,0,0

        self.warn = False
        self.id_group = id_group
        self.server = server
        self.token = token
        self.vel                      = '/v1/cmd_vel'
        self.jack_up_down             = '/v1/jack_up'
        self.follow                   = '/v1/follow'
        self.mobile_platform_move     = '/v1/mobile_platform_move'
        self.mobile_platform_send     = '/v1/mobile_platform_send'
        self.mobile_platform_pressure = '/v1/mobile_platform_pressure'
        self.move_                    = '/v1/move'
        self.mission_cancel           = '/v1/mission_cancel'
        self.odom                     ='/v1/robot_odom'
        self.mission_execute          = '/v1/mission_execute'
        self.mission_execute_mutli    = '/v1/mission_execute_mutli'
        self.mission                  = '/v1/missions'
        self.camera_back              = '/v1/camera_back'
        self.camera                   = '/v1/camera'
        self.robot_poses              = '/v1/robot_poses'

        self.labe11 = tk.Label(self.master, text='移载式可重构对接控制系统 ', width='75', bg='blue',font=('黑体', 20)).place(x=1, y=30)

        self.labe12 = tk.Label(self.master, text='1#移载单元', width='16', bg='light yellow').place(x=200, y=70)
        self.labe13 = tk.Label(self.master, text='2#移载单元', width='16', bg='light yellow').place(x=350, y=70)
        self.labe14 = tk.Label(self.master, text='3#移载单元', width='16', bg='light yellow').place(x=500, y=70)

        self.labe41 = tk.Label(self.master, text='定位器坐标', width='14', bg='light green').place(x=50, y=100)
        self.labe31 = tk.Label(self.master, text='定位器受力', width='14', bg='light green').place(x=50, y=150)
        self.x_platform_label = tk.Label(self.master, text='X轴坐标设定：', bg='light green',width=14).place( x=50, y=200)
        self.y_platform_label = tk.Label(self.master, text='y轴坐标设定：', bg='light green',width=14).place( x=50, y=250)
        self.z_platform_label = tk.Label(self.master, text='z轴坐标设定：', bg='light green',width=14).place( x=50, y=300)
        self.t_platform_label = tk.Label(self.master, text='运行时间: ', bg='light green', width=14).place(x=50, y=350)
        self.t_poge_moveset_label = tk.Label(self.master, text='旋转角度设定: ', bg='light green', width=14).place(x=50,
                                                                                                              y=750)
        self.coordinator = tk.Button(self.master, text='定位器绝对移动',bg='light blue', width='16', command=self.move_poge_all).place(
            x=500, y=350)
        self.labe21 = tk.Label(self.master, text='AGV平移速度', width='14', bg='light green').place(x=50, y=450)

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
        self.dis_move_rel = tk.StringVar()
        self.dis_move_rel.set("0.0")
        self.rotary = tk.StringVar()
        self.rotary.set("1.57")
        self.angular = tk.StringVar()
        self.angular.set("0.0")
        self.x1_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.x1_coord).place(x=200,
                                                                                                                  y=200)
        self.x2_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.x2_coord).place(x=350,
                                                                                                                  y=200)
        self.x3_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.x3_coord).place(x=500,
                                                                                                                  y=200)
        self.y1_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.y1_coord).place(x=200,
                                                                                                                  y=250)
        self.y2_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.y2_coord).place(x=350,
                                                                                                                  y=250)
        self.y3_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.y3_coord).place(x=500,
                                                                                                                  y=250)
        self.z1_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.z1_coord).place(x=200,
                                                                                                                  y=300)
        self.z2_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.z2_coord).place(x=350,
                                                                                                                  y=300)
        self.z3_coord_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.z3_coord).place(x=500,
                                                                                                                  y=300)
        self.t_num_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.t_num).place(x=200,
                                                                                                            y=350)
        self.rotary_ent = tk.Entry(self.master, width=16, font=('Arial', 10), textvariable=self.rotary).place(x=200,
                                                                                                            y=750)

        self.agv1_speed=tk.StringVar()
        self.agv1_speed.set('0.0')
        self.agv1_speed_box=tk.Entry(self.master, width=16, font=('Arial', 10),textvariable=self.agv1_speed).place(x=200, y=450)

        self.agv1_sensor=tk.StringVar()
        self.agv1_sensor.set('1#定位器当前受力')
        self.agv1_sensor_box=tk.Entry(self.master,width=16, font=('Arial', 10),bg='light gray', textvariable=self.agv1_sensor).place(x=200,y=150)

        self.agv1_coord=tk.StringVar()
        self.agv1_coord.set('1#定位器当前坐标')
        self.agv1_coord_box=tk.Entry(self.master,width=16, font=('Arial', 10),bg='light gray', textvariable=self.agv1_coord).place(x=200,y=100)

        self.agv2_sensor=tk.StringVar()
        self.agv2_sensor.set('2#定位器当前受力')
        self.agv2_sensor_box=tk.Entry(self.master,width=16, font=('Arial', 10),bg='light gray', textvariable=self.agv2_sensor).place(x=350,y=150)

        self.agv2_coord=tk.StringVar()
        self.agv2_coord.set('2#定位器当前坐标')
        self.agv2_coord_box=tk.Entry(self.master,width=16, font=('Arial', 10),bg='light gray', textvariable=self.agv2_coord).place(x=350,y=100)

        self.agv3_sensor=tk.StringVar()
        self.agv3_sensor.set('3#定位器当前受力')
        self.agv3_sensorr_box=tk.Entry(self.master,width=16, font=('Arial', 10),bg='light gray', textvariable=self.agv3_sensor).place(x=500,y=150)

        self.agv3_coord=tk.StringVar()
        self.agv3_coord.set('3#定位器当前坐标')
        self.agv3_coord_box=tk.Entry(self.master,width=16, font=('Arial', 10), bg='light gray',textvariable=self.agv3_coord).place(x=500,y=100)
        self.f_c_flag=tk.IntVar()
        self.routine = tk.Button(self.master, text='自动寻迹',bg='light blue', width='16', command=self.all_start).place(
            x=400, y=800)
        self.initposition = tk.Button(self.master, text='初始化寻迹',bg='light blue', width='16', command=self.all_start_position).place(
            x=600, y=800)
        self.initposition = tk.Button(self.master, text='归位',bg='light blue', width='16', command=self.non_all_start).place(
            x=800, y=800)

        self.direction=1.0
        self.fx_sum1=0
        self.fy_sum1=0
        self.f_sum1={1:self.fx_sum1,2:self.fy_sum1}
        self.fx_sum2=0
        self.fy_sum2=0
        self.f_sum2={1:self.fx_sum2,2:self.fy_sum2}
        self.fx_sum3=0
        self.fy_sum3=0
        self.f_sum3={1:self.fx_sum3,2:self.fy_sum3}
        self.f_sum={1:self.f_sum1,2:self.f_sum2,3:self.f_sum3}

        self.speed = {1:self.agv1_speed,2:self.agv1_speed,3:self.agv1_speed}
        self.sensor = {1:self.agv1_sensor,2:self.agv2_sensor,3:self.agv3_sensor}
        self.x_coord = {1: self.x1_coord, 2: self.x2_coord, 3: self.x3_coord}
        self.y_coord = {1: self.y1_coord, 2: self.y2_coord, 3: self.y3_coord}
        self.z_coord = {1: self.z1_coord, 2: self.z2_coord, 3: self.z3_coord}
        self.coord = {1:self.agv1_coord,2:self.agv2_coord,3:self.agv3_coord}
        self.fx = {1:0,2:0,3:0}
        self.fy = {1:0,2:0,3:0}
        self.record = {1:{'x':[],'y':[],'t':[]},2:{'x':[],'y':[],'t':[]},3:{'x':[],'y':[],'t':[]}}
        self.pogo_coord = {1:{'x':0,'y':0,'z':0},2:{'x':0,'y':0,'z':0},3:{'x':0,'y':0,'z':0}}

    def non_all_start(self):
        '''
        一键归位
        '''
        self.stop = 0
        t13 = Thread(target=self.startread)
        t14 = Thread(target=self.start_two)
        t13.start(), t14.start()

    def start_two(self):
        '''
        归位移动过程启动
        '''
        # ang = -1.0 * float(self.rotary.get())
        ang = float(self.rotary.get())
        self.move_pogo_startz(self.nzcord)
        self.move_pogo_starty(self.nycord)
        self.move_pogo_startx(self.nxcord)
        self.flag = 1
        # 随动到正向
        t_f1 = Thread(target=self.follow_three, args=(1, -3.14,))
        t_f2 = Thread(target=self.follow_three, args=(2, -3.14,))
        t_f3 = Thread(target=self.follow_three, args=(3, -3.14,))
        t_f1.start(), t_f2.start(), t_f3.start()
        t_f1.join(), t_f2.join(), t_f3.join()
        del t_f1, t_f2, t_f3
        time.sleep(15.0)
        # 开启报警
        t14 = Thread(target=self.tik, args=(1,))
        t15 = Thread(target=self.tik, args=(2,))
        t16 = Thread(target=self.tik, args=(3,))
        # 开启力控制
        t7 = Thread(target=self.force_control, args=(1,))
        t8 = Thread(target=self.force_control, args=(2,))
        t9 = Thread(target=self.force_control, args=(3,))
        # 开始移动
        t4 = Thread(target=self.move, args=(1, self.ycar,))
        t5 = Thread(target=self.move, args=(2, self.ycar,))
        t6 = Thread(target=self.move, args=(3, self.ycar,))
        t14.start(), t15.start(), t16.start()
        t7.start(), t8.start(), t9.start()
        t4.start(), t5.start(), t6.start()
        t4.join(), t5.join(), t6.join()
        del t4, t5, t6
        # 移动完后随动
        t1 = Thread(target=self.follow_three, args=(1, -ang,))
        t2 = Thread(target=self.follow_three, args=(2, -ang,))
        t3 = Thread(target=self.follow_three, args=(3, -ang,))
        t1.start(), t2.start(), t3.start()
        t1.join(), t2.join(), t3.join()
        del t1, t2, t3
        # 随动之后继续前进
        t10 = Thread(target=self.move, args=(1, self.xcar,))
        t11 = Thread(target=self.move, args=(2, self.xcar,))
        t12 = Thread(target=self.move, args=(3, self.xcar,))  
        t10.start(), t11.start(), t12.start()
        t10.join(), t11.join(), t12.join()
        del t10, t11, t12
        self.flag = 0
        time.sleep(0.5)
        self.move_pogo_startz_new(self.nzfirst) # 放下机翼
        self.move_poge_all() # 三轴归零
        t_e1 = Thread(target=self.follow_three, args=(1, 3.14))
        t_e2 = Thread(target=self.follow_three, args=(2, 3.14))
        t_e3 = Thread(target=self.follow_three, args=(3, 3.14))
        t_e1.start(), t_e2.start(), t_e3.start()

    def all_start_position(self):
        '''
        初始化循迹，从休息位置移动到目标点并通过相机找到球窝
        '''
        # 服务器任务移动
        t1 = Thread(target=self.mission_move)
        t1.start() 
        t1.join()
        del t1
        t4 = Thread(target=self.read_move, args=(1, 200, 3, 5000,))
        t5 = Thread(target=self.read_move, args=(2, 110, 3, 5000,))
        t6 = Thread(target=self.read_move, args=(3, 0, 3, 5000,))
        t4.start(), t5.start(), t6.start()
        t4.join(), t5.join(), t6.join()
        del t4, t5, t6
        # 相机寻找球窝
        t7 = Thread(target=self.camera_, args=(1,))
        t8 = Thread(target=self.camera_, args=(2,))
        t9 = Thread(target=self.camera_, args=(3,))
        t7.start(), t8.start(), t9.start()
        t7.join(), t8.join(), t9.join()
        del t7, t8, t9
        t10 = Thread(target=self.adapt, args=(1, -10, -2, 5,))
        t11 = Thread(target=self.adapt, args=(2, -4, 15, 5,))
        t13 = Thread(target=self.adapt, args=(3,-1,-9,-5,))
        t10.start(), t11.start(), t13.start()
        t10.join(), t11.join(), t13.join()
        del t10, t11, t13
        # 插轴入孔
        t14 = Thread(target=self.adapt_z, args=(1,))
        t15 = Thread(target=self.adapt_z, args=(2,))
        t16 = Thread(target=self.adapt_z, args=(3,))
        t14.start(), t15.start(), t16.start()
        t14.join(), t15.join(), t16.join()
        del t14, t15, t16
        print("preparing over...")

    def adapt_z(self, id_):
        '''
        通过力顺应插轴入孔
        Args:
            id_: robot_id
        '''
        while req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,'token' : self.token}).json()['data']['z']<50.:
            self.read_move(id_,4.0,3,1000)
            force_x=req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,'token' : self.token}).json()['data']['x']
            force_y=req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,'token' : self.token}).json()['data']['y']
            while abs(force_x) > 20.0:
                self.read_move(id_,abs(force_x)/force_x,1,1000)
                force_x =req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,'token' : self.token}).json()['data']['x']
            while abs(force_y) >20.0:
                self.read_move(id_,abs(force_y)/force_y,2,1000)
                force_y =req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,'token' : self.token}).json()['data']['y']
        # print("force_x",force_x)
        # print("force_y",force_y)
        # print("force_z",req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,'token' : self.token}).json()['data']['z'])

    def adapt(self, id_, normalx, normaly, normalz):
        '''
        相机通过标定寻找位置
        Args:
            id_: robot_id
            normalx, normaly, normalz: 相机标定值
        '''
        data = req.post(self.server + self.camera_back, json={'token': self.token, 'robot_id':self.id_group[id_]['robot_id']}).json()['data']
        dis_x = data['x']
        dis_y = data['y']
        ang_z = data['z']
        # print("id", id_)
        # print("dis_x:",dis_x)
        # print("dis_y",dis_y)
        while abs(dis_x-normalx) > 1.0:
            self.read_move(id_, dis_x-normalx, 1, 1000)
            data = req.post(self.server + self.camera_back, json={'token': self.token, 'robot_id':self.id_group[id_]['robot_id']}).json()['data']
            dis_x = data['x']
            dis_y = data['y']
            ang_z = data['z']
            print("dx=",dis_x-normalx)
        while abs(dis_y-normaly) > 1.0:
            self.read_move(id_, dis_y-normaly, 2, 1000)
            data = req.post(self.server + self.camera_back, json={'token': self.token, 'robot_id':self.id_group[id_]['robot_id']}).json()['data']
            dis_x = data['x']
            dis_y = data['y']
            ang_z = data['z']
            print("dy=",dis_y-normaly)
        job = req.post(self.server + self.camera, json={'token': self.token, 'robot_id':self.id_group[id_]['robot_id'],'up':False})

    def mission_move(self):
        '''
        发送任务点移动
        '''
        job1 = req.post(self.server + self.mission_execute, json={'token': self.token, 'robot_id':self.id_group[1]['robot_id'], 'id':7})
        time.sleep(5)
        job2 = req.post(self.server + self.mission_execute, json={'token': self.token, 'robot_id':self.id_group[2]['robot_id'], 'id':6})
        time.sleep(5)
        job3 = req.post(self.server + self.mission_execute, json={'token': self.token, 'robot_id':self.id_group[3]['robot_id'], 'id':5})
        while True:
            job = req.post(self.server + self.mission, json={'token': self.token,'page':0,'num':3})
            # print(job)
            text1,text2,text3=job.json()["data"]["data"][0]["status"],job.json()["data"]["data"][1]["status"],job.json()["data"]["data"][2]["status"]
            print("text1 = ",text1)
            print("text2 = ",text2)
            print("text3 = ",text3)
            if text1 == 2 and text2 == 2 and text3 == 2:
                break

    def camera_(self, id_):
        '''
        打开相机寻找球窝
        Args: 
            id_: robot_id
        '''
        job1 = req.post(self.server + self.camera, json={'token': self.token, 'robot_id':self.id_group[id_]['robot_id'],'up':True})
        job2 = req.post(self.server + self.camera_back, json={'token': self.token,'robot_id':self.id_group[id_]['robot_id']})
        data = job2.json()
        i = 0
        while data["data"]["stride"]==0:
            if i <= 20:
                self.read_move(id_, 1.0, 3)
            else:
                self.read_move(id_, -1.0, 3)
            i+=1
            data = job2.post(self.server + self.camera_back, json={'token':self.token, 'robot_id':self.id_group[id_]['robot_id']}).json()

    def read_move(self, id_, dis_, num, t):
        '''
        初始时摄像头升高
        Args:
            id_: robot_id
            dis_: 移动距离
            num: 轴编号，x,y,z -> 1,2,3
            t: 时间
        '''
        job1 = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                        'token': self.token})
        b = [0,0,0]  
        b[num-1] = 1                                         
        x = job1.json()['data']['x']
        y = job1.json()['data']['y']
        z = job1.json()['data']['z']
        job2 = req.post(self.server + self.mobile_platform_send,
                        json={'t': t, 'x': x+b[0]*dis_,
                              'y': y+b[1]*dis_, 'z':z+b[2]*dis_,
                              'id': id_, 'token': self.token})
        # print("xyz:",job2.text)
        while True:
            job3 = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                        'token': self.token})
            data=job3.json()['data']
            # print("xyz_coord:",job1.text)
            if abs(x+dis_*b[0]-data['x'])<0.1 and abs(y+dis_*b[1]-data['y'])<0.1 and abs(z+dis_*b[2]-data['z'])<0.1:
                break

    #auto routines
    def all_start(self):
        '''
        自动循迹开始
        '''
        self.move_pogo_startz_new(self.zfirst) # 
        t1 = Thread(target=self.startread)
        t2 = Thread(target=self.thread_start, args=(self.xcar,))
        t1.start()
        t2.start()

    def startread(self):
        '''
        读取三个AGV信息
        '''
        print("yes")
        t1 = Thread(target=self.read_sensor, args=(1,))
        t2 = Thread(target=self.read_sensor, args=(2,))
        t3 = Thread(target=self.read_sensor, args=(3,))
        t4 = Thread(target=self.read_coord, args=(1,))
        t5 = Thread(target=self.read_coord, args=(2,))
        t6 = Thread(target=self.read_coord, args=(3,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

    def thread_start(self, dis):
        '''
        线程开启，移动+急停报警+力控制。
        Args:
            dis: 移动距离
        '''
        t1 = Thread(target=self.move, args=(1, dis))
        t2 = Thread(target=self.move, args=(2, dis))
        t3 = Thread(target=self.move, args=(3, dis))
        t4 = Thread(target=self.tik, args=(1,))
        t5 = Thread(target=self.tik, args=(2,))
        t6 = Thread(target=self.tik, args=(3,))
        t7 = Thread(target=self.force_control, args=(1,))
        t8 = Thread(target=self.force_control, args=(2,))
        t9 = Thread(target=self.force_control, args=(3,))
        t1.start(), t2.start(), t3.start()
        t4.start(), t5.start(), t6.start()
        t7.start(), t8.start(), t9.start()
        t1.join(), t2.join(), t3.join()
        del t1, t2, t3
        ang = float(self.rotary.get())
        time.sleep(0.5)
        self.move_poge(ang)

    def tik(self, id_):
        '''
        急停功能，力超过限制急停发送急停指令
        Args:
            id_: robot_id
        '''
        while True:
            if self.warn:
                self.warn=False
                self.flag = 0
                self.end = True   
                job = req.post(self.server + self.mission_cancel, json={'token': self.token,
                                                                        'robot_id':self.id_group[id_]['robot_id'] })

                while job.json()["data"]!="success":
                    job = req.post(self.server + self.mission_cancel, json={'token': self.token,
                                                                            'robot_id': self.id_group[id_]['robot_id']})
                # self.warn=False
                print("WARNING")
                print("warn:",job.text)
                job1 = req.post(self.server + self.robot_poses, json={'token': self.token,'robot_id':self.id_group[id_]['robot_id']})
                data = job1.json()["data"]
                x = data['x']
                y = data['y']
                print("coord of {:d},x = {:.5f},y = {:.5f}".format(id_,x,y)) 
            if self.stop == 1:
                break
   
    def move(self, id_, dis):
        '''
        AGV直线移动
        Args:
            id_: robot_id
            dis: 移动距离
        '''
        if self.end:
            return
        speed = float(self.agv1_speed.get())

        dis_ = dis

        job2 = req.post(self.server + self.move_, json={'token': self.token,
                                                        'distance' : dis_,
                                                        'speed' : speed,
                                                        'robot_id' :self.id_group[id_]['robot_id']})
        print("move:",job2.text)
        time.sleep(0.5)
        while True:
            job1 = req.post(self.server + self.odom,
                            json={'token': self.token, 'id': self.id_group[id_]['robot_id']})
            data1 = job1.json()["data"]["linear_x"]
            # print("move_v:",job1.text)
            # print("data1:",data1)
            if data1==0:
                break

    def move_poge_all(self):
        '''
        定位器绝对移动
        '''
        job1 = req.post(self.server + self.mobile_platform_send,
                        json={'t': float(self.t_num.get()), 'x': float(self.x_coord[1].get()),
                              'y': float(self.y_coord[1].get()), 'z': float(self.z_coord[1].get()),
                              'id': 1, 'token': self.token})
        job2 = req.post(self.server + self.mobile_platform_send,
                        json={'t': float(self.t_num.get()), 'x': float(self.x_coord[2].get()),
                              'y': float(self.y_coord[2].get()), 'z': float(self.z_coord[2].get()),
                              'id': 2, 'token': self.token})
        job3 = req.post(self.server + self.mobile_platform_send,
                        json={'t': float(self.t_num.get()), 'x': float(self.x_coord[3].get()),
                              'y': float(self.y_coord[3].get()), 'z': float(self.z_coord[3].get()),
                              'id': 3, 'token': self.token})

    def move_poge(self, ang):
        '''
        三轴相对转动后移动
        Args:
            ang: 相对移动角度
        '''
        # 相对转动
        t1 = Thread(target=self.follow_three, args=(1, ang,))
        t2 = Thread(target=self.follow_three, args=(2, ang,))
        t3 = Thread(target=self.follow_three, args=(3, ang,))
        t1.start(), t2.start(), t3.start()
        t1.join(), t2.join(), t3.join()
        del t1, t2, t3
        # time.sleep(0.5)
        # 直线运动
        t4 = Thread(target=self.move, args=(1, self.ycar,))
        t5 = Thread(target=self.move, args=(2, self.ycar,))
        t6 = Thread(target=self.move, args=(3, self.ycar,))
        t4.start(), t5.start(), t6.start()
        t4.join(), t5.join(), t6.join()
        del t4, t5, t6
        # while self.warn:
        #     pass
        self.flag = 0
        time.sleep(0.5)
        self.move_pogo_startz(self.zcord)
        # time.sleep(0.5)
        self.move_pogo_starty(self.ycord)
        # time.sleep(0.5)
        self.move_pogo_startx(self.xcord)
        # self.flag=1
        self.stop = 1

    def follow_three(self, id_, ang):
        '''
        三轴平台相对移动
        Args:
            id_: robot_id
            ang: 三轴相对移动角度
        '''
        if self.end:
            return
        job = req.post(self.server + self.follow, json={'token': self.token,
                                                                    'follow':ang, 'robot_id' : self.id_group[id_]['robot_id'] })
        while True:
            job1 = req.post(self.server + self.odom,
                            json={'token': self.token, 'id': self.id_group[id_]['robot_id']})
            data=job1.json()['data']['angular_z']
            # print("follow_v:",job1.text)
            if data==0:
                break

    def move_pogo_startx(self, dis):
        t1 = Thread(target=self.move_poge_rel, args=(1, 1, dis,))
        t2 = Thread(target=self.move_poge_rel, args=(2, 1, dis,))
        t3 = Thread(target=self.move_poge_rel, args=(3, 1, dis,))
        t1.start()
        t2.start()
        t3.start()
        t1.join(), t2.join(), t3.join()
        del t1, t2, t3

    def move_pogo_starty(self, dis):
        t1 = Thread(target=self.move_poge_rel, args=(1, 2, dis,))
        t2 = Thread(target=self.move_poge_rel, args=(2, 2, dis,))
        t3 = Thread(target=self.move_poge_rel, args=(3, 2, dis,))
        t1.start()
        t2.start()
        t3.start()
        t1.join(), t2.join(), t3.join()
        del t1, t2, t3

    def move_pogo_startz(self, dis):
        t1 = Thread(target=self.move_poge_rel, args=(1, 3, dis,))
        t2 = Thread(target=self.move_poge_rel, args=(2, 3, dis,))
        t3 = Thread(target=self.move_poge_rel, args=(3, 3, dis,))
        t1.start()
        t2.start()
        t3.start()
        t1.join(), t2.join(), t3.join()
        del t1, t2, t3

    def move_pogo_startz_new(self, dis):
        '''
        '''
        # print("start",dis)
        t1 = Thread(target=self.move_poge_rel_new, args=(1, 3, dis,))
        t2 = Thread(target=self.move_poge_rel_new, args=(2, 3, dis,))
        t3 = Thread(target=self.move_poge_rel_new, args=(3, 3, dis,))
        t1.start()
        t2.start()
        t3.start()
        t1.join(), t2.join(), t3.join()
        del t1, t2, t3

    def move_poge_rel(self, id_, num, dis):
        t = float(self.t_num.get())
        # print("t_num.get():",t)
        x = self.pogo_coord[id_]['x']
        y = self.pogo_coord[id_]['y']
        z = self.pogo_coord[id_]['z']
        m = dis
        b = [0,0,0]
        b[num-1] = 1
        # print("success")
        job = req.post(self.server + self.mobile_platform_send,
                        json={'t': t, 'x': x+m*b[0],
                              'y': y+m*b[1], 'z':m*b[2]+z,
                              'id': id_, 'token': self.token})
        print("xyz:",job.text)
        while True:
            job1 = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                        'token': self.token})
            data = job1.json()['data']
            # print("xyz_coord:",job1.text)
            if abs(x+m*b[0]-data['x'])<0.1 and abs(y+m*b[1]-data['y'])<0.1 and abs(z+m*b[2]-data['z'])<0.1:
                break

    def move_poge_rel_new(self, id_, num, dis):
        '''
        '''
        print("start", id_)
        t = 5000
        print("time", t)
        job = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                        'token': self.token})
        print(job.text)
        data = job.json()['data']
        x = data['x']
        y = data['y']
        z = data['z']
        m = dis
        b = [0, 0, 0]
        b[num-1] = 1
        print("success")
        job = req.post(self.server + self.mobile_platform_send,
                        json={'t': t, 'x': x+m*b[0],
                              'y': y+m*b[1], 'z':m*b[2]+z,
                              'id': id_, 'token': self.token})
        print("xyz:",job.text)
        while True:
            job1 = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                        'token': self.token})
            data = job1.json()['data']
            print("xyz_coord:",job1.text)
            if abs(x+m*b[0]-data['x'])<0.1 and abs(y+m*b[1]-data['y'])<0.1 and abs(z+m*b[2]-data['z'])<0.1:
                break

    def scaling(self, f):
        f = f*0.1
        return f

    def pid(self, kp, ki, kd, f, df, id_, num):
        '''
        PID计算
        '''
        output = kp*f+ki*self.f_sum[id_][num]+kd*df
        return output

    def force_control(self, id_):
        '''
        力控制
        '''
        job1 = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                      'token': self.token})
        x = job1.json()['data']['x']
        y = job1.json()['data']['y']
        z = job1.json()['data']['z']
        # x=self.pogo_coord[id_]['x']
        # y=self.pogo_coord[id_]['y']
        # z=self.pogo_coord[id_]['z']
        tim = 0
        while self.flag:
            job = req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,
                                                                            'token' : self.token})
            data = job.json()['data']
            fx=data['x']
            self.record[id_]['x'] += [fx]
            fy=data['y']
            self.record[id_]['y'] += [fy]
            self.record[id_]['t'] += [tim]
            self.sensor[id_].set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))
            if abs(data['x']) > 250 or abs(data['y']) > 250:
                self.warn = True
            if((abs(data['x'])>30 or abs(data['y'])>30)):
                fx_= self.scaling(fx)
                fy_= self.scaling(fy)
                dfx_ = fx_-self.fx[id_]
                dfy_ = fy_-self.fy[id_]
                self.f_sum[id_][1] += fx_
                self.f_sum[id_][2] += fy_
                self.fx[id_] = fx_
                self.fy[id_] = fy_
                kpx,kix,kdx = self.fuzzy_controller_x.output(fx_,dfx_)
                kpy, kiy, kdy = self.fuzzy_controller_x.output(fy_, dfy_)
                vx = self.pid(kpx,kix,kdx,fx_,dfx_,id_,1) 
                vy = self.pid(kpy,kiy,kdy,fy_,dfy_,id_,2)
                dis = 3
                if abs(vx) <= abs(vy):
                    dis_y = dis*vy/abs(vy)
                    time_ = dis/abs(vy)
                    dis_x = vx*time_
                    self.move_coord(id_, time_*1000, x+dis_x, y+dis_y, z)
                else:
                    dis_x = dis*vx/abs(vx)
                    time_ = dis/abs(vx)
                    dis_y = vy*time_
                    self.move_coord(id_, time_*1000, x+dis_x, y+dis_y, z)
                x = x+dis_x
                y = y+dis_y
            tim += 0.01
        # print("over")

    def move_coord(self, id_, t=2000., x=30., y=40., z=50.):
        '''
        三轴移动
        Args:
            id_: AGV id
            t: 移动时间，单位ms
            x, y, z: 移动量
        '''
        job = req.post(self.server + self.mobile_platform_send, json={'t': t,'x' : x, 'y' : y, 'z' : z,
                                                                    'id' : id_, 'token': self.token})
        # print("force_pid:",job.text)

    def read_coord(self, id_):
        '''
        读取三轴坐标值
        Args:
            id_: AGV ID
        '''
        while True:
            job = req.post(self.server + self.mobile_platform_move, json={'id': id_,
                                                                        'token': self.token})
            data = job.json()['data']
            self.pogo_coord[id_]['x'] = data['x']
            self.pogo_coord[id_]['y'] = data['y']
            self.pogo_coord[id_]['z'] = data['z']
            self.coord[id_].set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))
            if self.stop:
                break

    def read_sensor(self, id_):
        '''
        读取力传感器值
        Args:
            id_ : AGV ID
        '''
        i = 0
        while True:
            job = req.post(self.server + self.mobile_platform_pressure, json={'id' : id_,
                                                                            'token' : self.token})
            data = job.json()['data']
            fx = data['x']
            fy = data['y']
            t = data['timestamp']
            self.sensor[id_].set('x:{:3.2f}, y:{:3.2f}, z:{:3.2f}'.format(data['x'], data['y'], data['z']))
            if abs(data['x']) > 250 or abs(data['y']) > 250:
                self.warn = True
            i += 1
            if self.stop:
                break
            if self.plot_flag:
                print("sensor over")
                break

if __name__ == "__main__":
    server = 'http://192.168.7.254'
    token = 'NWQ7TKPAX8HC2cJDdfKFYH4kTbXAaSh4WNde4YBPSbXR5fRPji7C5hnbSD8HcpM23ABQMkKACdWrEFMkE3mfS3kFRPJYKKbzi36e2RtPyBMTCbJaRDGbCBWrX3i7FFrb'
    robot_id_group = {1 : {'robot_id':'W50020190812003', 'id_':1},
                      2 : {'robot_id':'W50020190703001', 'id_':2},
                      3 : {'robot_id':'W50020190812002', 'id_':3}}

    test = three_all_change(tk.Tk(), server, token, robot_id_group, zfirst=0, xcar=1.5, ycar=1.0, xcord=0, ycord=0, zcord=0,
    nxcord=0, nycord=0., nzcord=0, nxcar=0., nycar=0., nzfirst=0)
    test.master.mainloop()
