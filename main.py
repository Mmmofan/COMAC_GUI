# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tm
from control import Controller
import requests as req

class Application(object):
    def __init__(self, root):
        # 定义主窗口
        self.master = root
        self.master.title('COMAC_04')
        self.master.geometry('500x300')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')

        # 定义私有量
        self.cond = False
        self.server = 'http://192.168.7.254'
        self.vel = '/v1/cmd_vel'
        self.jack_up_down = '/v1/jack_up'
        self.follow = '/v1/follow'
        self.token = 'NWQ7TKPAX8HC2cJDdfKFYH4kTbXAaSh4WNde4YBPSbXR5fRPji7C5hnbSD8HcpM23ABQMkKACdWrEFMkE3mfS3kFRPJYKKbzi36e2RtPyBMTCbJaRDGbCBWrX3i7FFrb'
        self.robot_id = 'W50020190812003'

        # 定义组件/按键
        # check  button
        self.check_button = ttk.Button(self.master, text='Check', width=15, command=self.check_func)
        self.check_button.place(x=45, y=70)
        # quit button
        self.quit_button = ttk.Button(self.master, text='Quit', width=15, command=self.quit_func)
        self.quit_button.place(x=45, y=220)
        # info text
        self.info_txt = tk.Label(self.master, text='Infomations:', bg='white', font=('Arial', 14), width=10, height=2).place(x=180, y=10)
        # address
        self.address_txt = tk.Label(self.master, text='Server Address:', bg='white', font=('Arial', 11), width=15, height=2).place(x=190, y=50)
        self.address = tk.Entry(self.master, show=None, width=20, font=('Arial', 10))
        self.address.place(x=200, y=80)
        self.address.insert(8, self.server)
        # Token
        self.port_txt = tk.Label(self.master, text='Token', bg='white', font=('Arial', 11), width=10, height=2).place(x=190, y=100)
        self.token_bt = tk.Entry(self.master, show=None, width=20, font=('Arial', 11))
        self.token_bt.place(x=200, y=130)
        self.token_bt.insert(8, self.token)
        # Robot id
        self.robot_id_txt = tk.Label(self.master, text='Robot id', bg='white', font=('Arial', 11), width=10, height=2).place(x=190, y=150)
        self.robot_id_en = tk.Entry(self.master, show=None, width=20, font=('Arial', 11))
        self.robot_id_en.place(x=200, y=180)
        self.robot_id_en.insert(8, self.robot_id)
        # update button
        self.connect = ttk.Button(self.master, text='Update', width=10, command=self.update)
        self.connect.place(x=380, y=70)


    def check_func(self):
        '''
        检查服务器连接状态、以及其他状态是否正确
        '''
        # 尝试连接服务器，若无法连接提示错误
        try:
            r = req.get(self.server)
        except:
            # raise Exception('Invalid Server')
            tm.showerror(title='INVALID', message='Invalid Server')
            return

        # self.cond 可以再做修改，添加状态检测，目前设置为True
        self.cond = True
        # 提示是否进入控制模式
        if self.cond:
            enter = tm.askquestion(title='Checked!', message='Enter Control Mode?')
        if enter == 'no':
            pass
        else:
            self.master.destroy()
            # 进入控制模式
            robot_id = self.robot_id
            token = self.token
            server = self.server
            jack_up = self.jack_up_down
            vel = self.vel
            follow = self.follow
            root = tk.Tk()
            controller = Controller(root, robot_id, token, server, jack_up, vel, follow)
            controller.master.mainloop()
 
    def quit_func(self):
        '''
        退出，关闭GUI
        '''
        self.master.destroy()

    def update(self):
        '''
        更新服务器地址
        '''
        # 获取新的输入值
        robot_id = self.robot_id_en.get()
        token = self.token_bt.get()
        server = self.address.get()

        # 判断是否和原先一样
        if robot_id != self.robot_id:
            self.robot_id = robot_id
        if token != self.token:
            self.token = token
        if server != self.server:
            self.server = server
        # 提示更新完成
        tm.messagebox(title='UPDATE', message='Server updated!')


if __name__ == "__main__":
    root = tk.Tk()
    window = Application(root)
    window.master.mainloop()
