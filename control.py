# -*- coding: utf-8 -*-
import os
import tkinter as tk
import tkinter.messagebox as tm
from tkinter import ttk
from PIL import Image, ImageTk

# 控制模式界面
class Controller(object):
    def __init__(self, root, robot_id, token, server, id_):
        # 定义主窗口
        self.master = root
        self.master.title('COMAC_04')
        self.master.geometry('1000x600')
        self.master.resizable(width=False, height=False)
        self.master.configure(background='white')

        # 定义私有量
        self.server = server
        self.token = token
        self.robot_id = robot_id
        self.id_ = id_
        self.jack_up = '/v1/jack_up'
        self.vel = '/v1/cmd_vel'
        self.follow = '/v1/follow'
        self.mobile_platform_move = '/v1/mobile_platform_move'
        self.mobile_platform_send = '/v1/mobile_platform_send'
        self.mobile_platform_pressure = '/v1/mobile_platform_pressure'

        # 定义基本按键
        # step 1 (Button + image)
        self.button_1 = ttk.Button(self.master, text='Follow', width='16', command=self.func_1)
        self.button_1.place(x=70, y=60)
        self.img1 = self.image(os.path.join('pic','step1.png'))
        self.imLabel1 = tk.Label(self.master, image=self.img1).place(x=230, y=30)

        # step 2 (Button + image)
        self.button_2 = ttk.Button(self.master, text='Go!', width='16', command=self.func_2)
        self.button_2.place(x=70, y=160)
        self.button_2.state(['disabled'])
        self.img2 = self.image(os.path.join('pic','step2.png'))
        self.imLabel2 = tk.Label(self.master, image=self.img2).place(x=230, y=130)

        # step 3 (Button + image)
        self.button_3 = ttk.Button(self.master, text='Up&Down', width='16', command=self.func_3)
        self.button_3.place(x=70, y=260)
        self.button_3.state(['disabled'])
        self.img3 = self.image(os.path.join('pic','step3.png'))
        self.imLabel3 = tk.Label(self.master, image=self.img3).place(x=230, y=230)

        # step 4 (Button + image)
        self.button_4 = ttk.Button(self.master, text='Move&Rotate', width='16', command=self.func_4)
        self.button_4.place(x=70, y=360)
        self.button_4.state(['disabled'])
        self.img4 = self.image(os.path.join('pic','step4.png'))
        self.imLabel4 = tk.Label(self.master, image=self.img4).place(x=230, y=330)

        # step 5 (Button + image)
        self.button_5 = ttk.Button(self.master, text='Coordinator', width='16', command=self.func_5)
        self.button_5.place(x=70, y=460)
        self.button_5.state(['disabled'])
        self.img5 = self.image(os.path.join('pic','step5.png'))
        self.imLabel5 = tk.Label(self.master, image=self.img5).place(x=230, y=430)

        # quit button
        self.quit_button = ttk.Button(self.master, text='Quit', width='16', command=self.quit_func)
        self.quit_button.place(x= 860, y=550)
        self.done_job = False
        # reset button
        self.reset_but = ttk.Button(self.master, text='Reset', width='16', command=self.reset_func)
        self.reset_but.place(x=720, y=550)

    def image(self, img_path):
        '''
        读取图片，将图片resize到同一大小，输入图片路径，返回Image格式的图片数据
        '''
        img = Image.open(img_path)
        (width, height) = img.size
        image = img.resize((160, 80), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        return img

    def func_1(self):
        '''
        第一步功能，未完成
        '''
        self.button_1.state(['disabled'])
        self.button_2.state(['!disabled'])

    def func_2(self):
        '''
        第二步功能，未完成
        '''
        self.button_2.state(['disabled'])
        self.button_3.state(['!disabled'])

    def func_3(self):
        '''
        第三步功能，未完成
        '''
        self.button_3.state(['disabled'])
        self.button_4.state(['!disabled'])

    def func_4(self):
        '''
        第四步功能，未完成
        '''
        self.button_4.state(['disabled'])
        self.button_5.state(['!disabled'])

    def func_5(self):
        '''
        第五步功能，未完成
        '''
        self.button_5.state(['disabled'])
        self.done_job = True
        tm.showinfo(title='DONE', message='DONE!')

    def quit_func(self):
        '''
        退出按键，在未完成任务的情况下点击会出现提示
        '''
        if not self.done_job:
            cond = tm.askquestion(title='QUIT?', message='Job is not done, quit?')
        else:
            self.master.destroy()
            return

        if cond == 'no':
            pass
        else:
            self.master.destroy()

    def reset_func(self):
        '''
        任务完成后可以重置任务, 基本功能未完成
        '''
        cond = None
        if self.done_job:
            cond = tm.askquestion(title='RESET?', message='Reset?')
        else:
            tm.showwarning(title='WARNING', message='Not done yet')
        if cond == 'yes':
            self.button_1.state(['!disabled'])
            self.button_2.state(['disabled'])
            self.button_3.state(['disabled'])
            self.button_4.state(['disabled'])
        else:
            pass


if __name__ == "__main__":
    # args: root, robot_id, token, server, jack_up, vel, follow
    master  = Controller(tk.Tk(), 'W50020190812003', 'NWQ7TKPAX8HC2cJDdfKFYH4kTbXAaSh4WNde4YBPSbXR5fRPji7C5hnbSD8HcpM23ABQMkKACdWrEFMkE3mfS3kFRPJYKKbzi36e2RtPyBMTCbJaRDGbCBWrX3i7FFrb',
                        'http://192.168.7.254', 1)
    master.master.mainloop()

