# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 19:11
# @Author  : tanlei0
# @FileName: SheepDog.py
import numpy as np


class SheepDog:

    def __init__(self, coords, sheepGroup_coords, target, r_a, fN=27, speed=3, e=0.3, p=0.01, h=0.5, isTest=True, onNoise=True):
        assert (coords.shape == (1, 2))
        self.coords = coords
        n_sheep = sheepGroup_coords.shape[0]
        self.taget = target
        self.speed = speed
        self.r_a = r_a
        self.e = e
        self.p = p
        #获取中心点等测试参数
        self.isTest = isTest
        self.onNoise = onNoise
        self.fN = fN
        #self.fN = r_a * np.power(n_sheep, 2 / 3) / 3  # test
        # todo 记得 调整 位置
        self.onNoise = onNoise
        self.p_d = self.r_a * np.sqrt(n_sheep)
        self.p_c = self.r_a
        self.h = h
        # gai
        self.H_p = np.zeros(self.coords.shape, dtype=np.float64)
        self.H = np.zeros(self.coords.shape, dtype=np.float64)
        self.P = np.zeros(self.coords.shape, dtype=np.float64)

    def drivePosition(self, GCM):
        direction = self.taget - GCM
        direction = direction / np.linalg.norm(direction)
        drivePoistion = GCM - direction * self.p_d

        return drivePoistion

    def collectPosition(self, GCM, furCoords):

        direction = furCoords - GCM
        direction = direction / np.linalg.norm(direction)
        collectPosition = direction * self.p_c + furCoords
        # collectPosition = self.r_a + furCoords

        return collectPosition

    def action(self, sheepGroup_coords):

        GCM = self.getGCM(sheepGroup_coords)
        furCoords, furDistance = self.getFurthestSheep(sheepGroup_coords, GCM)
        if np.round(furDistance) > self.fN:
            self.Task = 'collect'
            self.P = self.collectPosition(GCM=GCM, furCoords=furCoords)
        else:
            self.Task = 'drive'
            self.P = self.drivePosition(GCM=GCM)

        H = self.P - self.coords
        H = H / np.linalg.norm(H)

        if self.onNoise is True:
            if np.random.uniform(0, 1) < self.p:
                noise = np.random.uniform(0, 999, [2, ])
                noise /= np.linalg.norm(noise)
                H += noise * self.e

        H += self.H_p * self.h
        H = H / np.linalg.norm(H)

        self.H_p = H

        speed = self.getSpeed(sheepGroup_coords)
        self.coords = self.coords + H * speed

        if self.isTest is True:
            TaskLabel = self.Task + (" fN:%d fur:%d dist:%d" % (
                int(self.fN), int(furDistance), int(np.linalg.norm(self.coords - GCM))))
            kwargs = {'P_GCM': GCM, 'TaskLabel': TaskLabel, 'P_an': self.P}
            return self.coords, kwargs
        else:
            return self.coords

    def getSpeed(self, sheepGroup_coords):
        # todo 改成函数式
        distance = np.zeros([sheepGroup_coords.shape[0], 1], dtype=np.float64)
        for i in range(sheepGroup_coords.shape[0]):
            distance[i] = np.linalg.norm(sheepGroup_coords[i] - self.coords)
        imin, vmin = distance.argmin(), min(distance)
        if vmin <= 3 * self.r_a:
            return self.speed / 2

        return self.speed

    @staticmethod
    def getFurthestSheep(sheepGroup_coords, GCM):
        distance = np.zeros([sheepGroup_coords.shape[0], 1])
        for i in range(sheepGroup_coords.shape[0]):
            distance[i] = np.linalg.norm(sheepGroup_coords[i] - GCM)
        imax, vmax = distance.argmax(), max(distance)
        return sheepGroup_coords[imax], vmax

    @staticmethod
    def getGCM(sheepGroup_coords):
        return sheepGroup_coords.mean(axis=0)
