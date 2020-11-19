# -*- coding: utf-8 -*-
# @Time    : 2018/11/2 13:39
# @Author  : tanlei0
# @FileName: SheepGroup.py
import numpy as np


class SheepGroup:
    def __init__(self, coords, r_a=6, e=0.3, c=1.2, ro_a=2, ro_s=1, r_s=65, p=0.05, h=0, speed=1, onNoise=True,
                 DistModel=True, Dlc=60):

        self.coords = coords
        self.kinds = np.zeros(coords.shape[0], dtype='I')  # 种类矩阵

        ################ 论文参数
        self.__r_a = r_a
        self.__e = e
        self.__c = c
        self.__ro_a = ro_a
        self.__ro_s = ro_s
        self.__r_s = r_s
        self.__p = p
        self.__h = h
        ############### 论文参数

        self.__speed = speed
        self.__H_p = np.zeros(coords.shape, dtype=np.float64) # 似乎是惯性值
        self.__onNoise = onNoise
        self.__DistModel = DistModel
        self.__Dlc = Dlc  # Dlc 是视距




    def __getA(self):
        # 羊群排斥力

        matA = np.zeros(self.coords.shape, dtype=np.float64)
        for i in range(self.coords.shape[0]):
            mat_temp = np.square(self.coords[i, :] - self.coords)
            mat_temp = np.sqrt(mat_temp[:, 0] + mat_temp[:, 1])
            assert (mat_temp.shape[0] == self.coords.shape[0])  # distance
            r_a_index = np.array(np.where(mat_temp <= self.__r_a)).reshape(-1).tolist()
            r_a_index.remove(i)
            if r_a_index == []:
                continue
            else:
                mat_temp = self.coords[r_a_index]

                up = self.coords[i, :].reshape(-1, self.coords.shape[1]) - mat_temp
                down = np.linalg.norm(self.coords[i, :] - mat_temp, axis=1).reshape(mat_temp.shape[0], -1)
                divide = up / down

                assert (np.isnan(divide).any() != True)

                matA[i, :] = np.sum(divide, axis=0)

        return matA

    def __getC(self, sheepDog_coords):
        # 中心力
        matC = np.zeros(self.coords.shape)
        matLC = self.__getLC()
        mat_temp = np.linalg.norm(sheepDog_coords - self.coords, axis=1)
        c_index = np.where(mat_temp <= self.__r_s)
        matC[c_index] = matLC[c_index] - self.coords[c_index]
        down = np.linalg.norm(matC, axis=1).reshape(matC.shape[0], -1)
        matC = matC / down
        matC = np.nan_to_num(matC)
        assert (np.isnan(matC).any() != True)
        return matC

    def __getLC(self):
        matLC = np.zeros(self.coords.shape)
        for i in range(self.coords.shape[0]):
            mat_temp = np.square(self.coords[i, :] - self.coords)
            mat_temp = np.sqrt(mat_temp[:, 0] + mat_temp[:, 1])
            assert (mat_temp.shape[0] == self.coords.shape[0])  # distance
            r_a_index = np.array(np.where(mat_temp <= self.__Dlc)).reshape(-1).tolist()
            mat_temp = self.coords[r_a_index]
            matLC[i, :] = mat_temp.mean(axis=0)

        return matLC


    def __getS(self, sheepDog_coords):
        # 羊狼排斥力
        # todo 修改为指数函数
        matS = np.zeros(self.coords.shape)
        mat_temp = np.linalg.norm(self.coords - sheepDog_coords, axis=1)
        # 当某一个羊的距离小于警戒距离，他就有了S向量
        s_index = np.where(mat_temp <= self.__r_s)
        matS[s_index] = self.coords[s_index] - sheepDog_coords
        down = np.linalg.norm(matS, axis=1).reshape(matS.shape[0], -1)
        matS = matS / down
        matS = np.nan_to_num(matS)
        assert (np.isnan(matS).any() != True)
        return matS

    def __getNoise(self):
        matP = np.random.uniform(0, 1, self.coords.shape[0])
        p_index = np.where(matP <= self.__p)
        matN = np.random.normal(size=self.coords.shape)
        mat_temp = np.array(matN)
        mat_temp[p_index, :] = 0
        matN = matN - mat_temp
        down = np.linalg.norm(matN, axis=1).reshape(matN.shape[0], -1)
        matN = matN / down
        matN = np.nan_to_num(matN)
        assert (np.isnan(matN).any() != True)
        return matN

    def __getInertia(self, sheepDog_coords, H):
        matI = np.zeros(self.coords.shape)
        mat_temp = np.linalg.norm(self.coords - sheepDog_coords, axis=1)
        i_index = np.where(mat_temp <= self.__r_s)
        matI[i_index] = H[i_index]
        return matI

    def __getRo_s(self, sheepDog_coords, maxV=4, minV=1):
        # max 4 , min 1
        k = (maxV - minV) / (self.__r_a - self.__r_s)
        ro_s = np.ones(shape=self.coords.shape) * self.__ro_s
        distance = np.linalg.norm(sheepDog_coords - self.coords, axis=1)
        f = k * distance - self.__r_s * k + minV
        ro_s[:, 0] = f
        ro_s[:, 1] = f

        return ro_s



    def action(self, sheepDog_coords):

        R_S = self.__getS(sheepDog_coords)
        C = self.__getC(sheepDog_coords)
        R_A = self.__getA()

        if self.__onNoise is True:
            Noise = self.__getNoise()
        else:
            Noise = 0

        if self.__DistModel is True:
            ro_s = self.__getRo_s(sheepDog_coords)
        else:
            ro_s = self.__ro_s

        H = self.__ro_a * R_A + ro_s * R_S + self.__c * C + self.__e * Noise + self.__h * self.__H_p

        H = H / np.linalg.norm(H, axis=1).reshape(H.shape[0], -1)
        H = np.nan_to_num(H)

        self.__H_p = self.__getInertia(sheepDog_coords, H)

        # todo 修改速度为函数式
        self.coords = self.coords + H * self.__speed

