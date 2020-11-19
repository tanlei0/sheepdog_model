# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 13:43
# @Author  : tanlei0
# @FileName: Canvas.py
import tkinter as tk
import numpy as np
import math


# 引入变量
from conf import GUIheight, GUIwidth
from conf import sheepRadius, dogRadius
from conf import endCircleRadius, endPoint
from conf import btnMenu_size

class Canvas(tk.Canvas):
    def __init__(self, window, width=GUIwidth, height=GUIheight):
        super().__init__(window, width=GUIwidth, height=GUIheight)

        self.__sheepRadius = sheepRadius
        self.__dogRadius = dogRadius
        self.__sheepGroupIDlist = []
        self.__sheepDogIDlist = []

        self.cursorCoords = np.zeros([1, 2], dtype='I')

        self.__coords_text = self.create_text(40, height-10-1.5*btnMenu_size[0], text="x: Null y: Null")

        self.bind(sequence='<Motion>', func=self.__mouse_moving)
        self.pack()

    def __mouse_moving(self, event):
        x0, y0 = event.x, event.y
        self.itemconfig(self.__coords_text, text="x: " + str(x0) + " y:" + str(y0))
        self.cursorCoords = np.array([[x0, y0]])

    def showPointsByKind(self, points, kinds):
        i = 0
        if kinds[0] != 'dog':
            if self.__sheepGroupIDlist == []:
                for p in points:
                    self.__sheepGroupIDlist.append(self.__createPointByKind(p, kinds[i]))
                    i += 1
            else:
                for p in points:
                    x1, y1, x2, y2 = Center2Points(p, self.__sheepRadius)
                    self.coords(self.__sheepGroupIDlist[i], x1, y1, x2, y2)
                    i += 1
        else:
            if self.__sheepDogIDlist ==[]:
                for p in points:
                    self.__sheepDogIDlist.append(self.__createPointByKind(p, kinds[i]))
                    i += 1
            else:
                for p in points:
                    x1, y1, x2, y2 = Center2Points(p, self.__dogRadius)
                    self.coords(self.__sheepDogIDlist[i], x1, y1, x2, y2)
                    i += 1


    def __createPointByKind(self, point, kind):
        # 0 color : green
        # 1 color : blue
        # dog color : black

        if kind == 'dog':
            color = 'black'
            ID = self.__createOvalBycenterPoint(point, self.__dogRadius, **{'fill': color})
            return ID

        if kind == 0:
            color = 'green'
        if kind == 1:
            color = 'blue'
        ID = self.__createOvalBycenterPoint(point, self.__sheepRadius, **{'fill': color})

        return ID

    def __createOvalBycenterPoint(self, centerPoint, r, **kwargs):
        x1, y1, x2, y2 = Center2Points(centerPoint, r)

        ID = self.create_oval(x1, y1, x2, y2, kwargs)

        return ID

    def drawEndCircle(self, color=''):
        self.__createOvalBycenterPoint(endPoint, endCircleRadius, **{'fill': color, 'tag': 'endCircle'})

    def clear(self):
        for i in self.__sheepGroupIDlist:
            self.delete(i)
        self.__sheepGroupIDlist = []
        for i in self.__sheepDogIDlist:
            self.delete(i)
        self.__sheepDogIDlist = []
        self.delete('endCircle')



def Center2Points(center, r):
    x1 = center[0] - r
    y1 = center[1] + r
    x2 = center[0] + r
    y2 = center[1] - r
    return x1, y1, x2, y2




