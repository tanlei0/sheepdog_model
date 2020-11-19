# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 16:00
# @Author  : tanlei0
# @FileName: MenuBar.py

from PIL import Image, ImageTk
import tkinter as tk
from Env import Env
import time
from TaskThread import TaskThread
import numpy as np
from conf import btnMenu_size



class MenuBar:
    def __init__(self, root):
        # 菜单
        self.root = root
        self.master = tk.Menu(self.root)
        Taskmenu = tk.Menu(self.master, tearoff=False)
        self.master.add_cascade(label='Task', menu=Taskmenu)
        Taskmenu.add_command(label='Start', command=self.fun_start)
        Taskmenu.add_command(label='Pause', command=self.fun_pause)
        Taskmenu.add_separator()
        Taskmenu.add_command(label="Quit", command=root.quit)

        Mousemenu = tk.Menu(self.master, tearoff=False)
        self.master.add_cascade(label='MouseJob', menu=Mousemenu)
        Mousemenu.add_command(label='Start', command=self.__fun_mouseJob)

        self.master.add_command(label='clear', command=self.fun_clear)

        root.config(menu=self.master)
    def fun_start(self):
        pass

    def fun_pause(self):
        pass

    def __fun_mouseJob(self):
        global t
        t = TaskThread(target=self.__mouse_update, args=[self.root.canvas, ])
        t.flag = 1
        t.start()

    def fun_test(self):
        pass

    def fun_clear(self):
        pass

    def __mouse_update(self, canvas):
        np.seterr(divide='ignore', invalid='ignore')
        env = Env(n_sheep = 30)
        canvas.drawEndCircle()
        while True:
            if t.flag == 0:
                print("stop")
                env.clear(canvas)
                break
            if t.flag == 1:

                canvas.showPointsByKind(env.sheepGroup.coords, env.sheepGroup.kinds)

                canvas.showPointsByKind(canvas.cursorCoords, ['dog'])

                env.sheepGroup.action(canvas.cursorCoords)

                time.sleep(0.01)

                if env.isGameOver() is True:
                    print("game over")
                    t.flag = 2
                    break

class BtnMenu:

    def __init__(self, topframe):
        self.topframe = topframe
        self.__initImage()
        self.__initBtn()

    def __initBtn(self):
        self.btnStop = tk.Button(self.topframe, image=self.image_btnstop, command=self.__fun_stop)
        self.btnPause = tk.Button(self.topframe, image=self.image_btnpause, command=self.__fun_pause)
        self.btnStart = tk.Button(self.topframe, image=self.image_btnstart, command=self.__fun_resume)

    def __initImage(self):
        self.image_btnstop = Image.open(r'image/stop2.png')
        self.image_btnstop = self.image_btnstop.resize(btnMenu_size)
        self.image_btnstop = ImageTk.PhotoImage(self.image_btnstop)

        self.image_btnpause = Image.open(r'image/pause.jpg')
        self.image_btnpause = self.image_btnpause.resize(btnMenu_size)
        self.image_btnpause = ImageTk.PhotoImage(self.image_btnpause)

        self.image_btnstart = Image.open(r'image/start.jpg')
        self.image_btnstart = self.image_btnstart.resize(btnMenu_size)
        self.image_btnstart = ImageTk.PhotoImage(self.image_btnstart)

    def __fun_stop(self):
        t.flag = 0
        print("click stop btn")

    def __fun_pause(self):
        t.flag = 2
        print("click pause btn")

    def __fun_resume(self):
        t.flag = 1
        print("click resume btn")

