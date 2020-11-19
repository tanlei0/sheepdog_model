# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 0:34
# @Author  : tanlei0
# @FileName: SetDialog.py
from PIL import Image
import tkinter as tk
from PIL import Image, ImageTk
from conf import GUIwidth
class SetDialog(tk.Toplevel):
    def __init__(self, parent, title="Setting", ):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        # 创建对话框的主体内容
        frame = tk.Frame(self)
        # 调用init_widgets方法来初始化对话框界面
        self.__init_image()
        self.initial_focus = self.__init_widgets(frame)
        frame.pack(padx=5, pady=5)
        #self.init_buttons()
        if not self.initial_focus:
            self.initial_focus = self

        # 根据父窗口来设置对话框的位置
        self.geometry("+%d+%d" % (parent.winfo_rootx() + GUIwidth + 100,
                                  parent.winfo_rooty() + 100))
        self.resizable(0, 0)
        # 通过该方法来创建自定义对话框的内容
    def __init_widgets(self, master):

        self.btnStop = tk.Button(master, image=self.image_btnstop).pack(side=tk.LEFT, fill=tk.Y)
        self.btnPause = tk.Button(master, image=self.image_btnpause).pack(side=tk.LEFT, fill=tk.Y)
        self.btnStart = tk.Button(master, image=self.image_btnstart).pack(side=tk.LEFT, fill=tk.Y)
    def __init_image(self):
        self.image_btnstop = Image.open(r'image/stop2.png')
        self.image_btnstop = self.image_btnstop.resize([40, 40])
        self.image_btnstop = ImageTk.PhotoImage(self.image_btnstop)

        self.image_btnpause = Image.open(r'image/pause.jpg')
        self.image_btnpause = self.image_btnpause.resize([40, 40])
        self.image_btnpause = ImageTk.PhotoImage(self.image_btnpause)

        self.image_btnstart = Image.open(r'image/start.jpg')
        self.image_btnstart = self.image_btnstart.resize([40, 40])
        self.image_btnstart = ImageTk.PhotoImage(self.image_btnstart)


