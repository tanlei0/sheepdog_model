# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 13:39
# @Author  : tanlei0
# @FileName: Env.py

from SheepGroup import SheepGroup
import numpy as np



# 引入一些变量
from conf import sheepRadius, dogRadius
from conf import GUIheight, GUIwidth
from conf import n_sheep
from conf import endPoint, endCircleRadius

def BounderCheck(Point):

    alter = dogRadius if dogRadius > sheepRadius else sheepRadius
    if Point[0] <= 0:
        Point[0] = alter
    if Point[1] <= 0:
        Point[1] = alter
    if Point[0] >= GUIwidth:
        Point[0] = GUIwidth - alter
    if Point[1] >= GUIheight:
        Point[1] = GUIheight - alter

    return Point


class Env:
    # rectPoint 左上和右下的坐标内随机生成agents
    def __init__(self, rectPoint1 = [50, 50], rectPoint2=[180, 180], n_sheep=n_sheep):
        self.n_sheep = n_sheep
        sheepGroupCoords = self.__InitSheepGroupCoords(rectPoint1, rectPoint2, self.n_sheep)
        self.sheepGroup = SheepGroup(sheepGroupCoords)


    def __InitSheepGroupCoords(self, rectPoint1, rectPoint2, n_sheep):
        x1 = rectPoint1[0] + sheepRadius
        x2 = rectPoint2[0] - sheepRadius
        y1 = rectPoint1[1] + sheepRadius
        y2 = rectPoint2[1] - sheepRadius

        [x1, y1] = BounderCheck([x1, y1])
        [x2, y2] = BounderCheck([x2, y2])

        MatX = np.random.randint(x1, x2, n_sheep)
        MatY = np.random.randint(y1, y2, n_sheep)

        Mat = np.array([MatX, MatY], dtype='I').transpose()

        # Mat.shape : [n_sheep, 2]

        assert Mat.shape == (n_sheep, 2)
        return Mat

    def step(self, sheepDog_coords):

        self.sheepGroup.action(sheepDog_coords=sheepDog_coords)

        # todo 不同模式下的GameOver
    def isGameOver(self):
        # 结束条件： 所有点进圈
        # temp : n_sheep个距离
        temp = np.linalg.norm(self.sheepGroup.coords - endPoint, axis=1)

        if (temp < endCircleRadius).all():
            return True
        else:
            return False

    def clear(self, canvas=''):
        self.sheepGroup = ''
        if canvas != '':
            canvas.clear()




