# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 20:08
# @Author  : tanlei0
# @FileName: GUI.py

import tkinter as tk
import time

from Canvas import Canvas
from MenuBar import MenuBar
from MenuBar import BtnMenu

from conf import GUIheight, GUIwidth
class Application(tk.Tk):
    '''
    文件夹选择程序
        界面与逻辑分离
    '''

    def __init__(self):
        '''初始化'''
        super().__init__()  # 有点相当于tk.Tk()

        self.__initWidgets()
        self.__initMenu(MenuBar)
    def __initWidgets(self):
        '''界面'''
        # 注意
        self.columnconfigure(0, minsize=50)

        #
        self.title("Sheepherd Simuulator")
        self.geometry(str(GUIwidth) + 'x' + str(GUIheight))
        self.resizable(0, 0)

        # 先定义顶部和内容两个Frame，用来放置下面的部件
        topframe = tk.Frame(self, height=80)
        contentframe = tk.Frame(self)
        topframe.pack(side=tk.TOP, anchor=tk.W)
        contentframe.pack(side=tk.TOP)

        # 顶部区域（四个部件）
        # -- 前三个直接用 tk 的 widgets，第四个下拉列表 tk 没有，ttk 才有，比较麻烦
        self.btnMenu = BtnMenu(topframe)

        # -- 放置位置
        self.btnMenu.btnStart.grid(row=0, column=0, ipadx=2)
        self.btnMenu.btnPause.grid(row=0, column=1, ipadx=2)
        self.btnMenu.btnStop.grid(row=0, column=2, ipadx=2)

        # 内容区域（三个部件）
        # -- 前两个滚动条一个竖直一个水平
        self.canvas = Canvas(contentframe)
        # -- 放置位置
        self.canvas.pack()

    def __initMenu(self, Menu):
        '''添加菜单'''
        Menu(self)


if __name__ == '__main__':
    # 实例化Application
    app = Application()

    # 主消息循环:
    app.mainloop()










