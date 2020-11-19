# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 15:47
# @Author  : tanlei0
# @FileName: Env2.py
import numpy as np
import math
from SheepGroup import SheepGroup
from SheepDog import SheepDog
from Viewer import Viewer


class Env(object):
    np.random.seed(1)

    def __init__(self, SheepGroup_info, SheepDog_info, fN=27, isRandom=False, isGetData=False,
                 test_SheepGroup_coords=None, test_SheepDog_coords=None, onNoise=True, Model=0, InitState=1):
        np.seterr(divide='ignore', invalid='ignore')
        self.viewer = None
        self.WIN_WIGHT = 1200
        self.WIN_HEIGHT = 700
        self.SheepGroup_info = SheepGroup_info
        self.SheepDog_info = SheepDog_info
        self.n_sheep = SheepGroup_info['n_sheep']
        self.n_dog = SheepDog_info['n_dog']  # 目前按数量为1考虑，后续需要再改代码
        self.r_a = SheepGroup_info['r_a']
        self.isRandom = isRandom
        self.fN = fN
        self.isGetData = isGetData
        self.kwargs = {}
        self.target = np.array([100, self.WIN_HEIGHT - 100], dtype=np.int32)
        self.test_SheepGroup_coords = None
        self.test_SheepDog_coords = None
        self.onNoise = onNoise
        self.Model = Model
        self.sheepGroupInitState = InitState
        # InitState : 0--集中分布, 1--散状分布
        # coordsInit
        self.coordsInit()



        if self.isGetData:
            self.dogTrace = []
            self.fur = []
            self.dogTrace.append(self.sheepDog.coords)
            self.initDistance = np.linalg.norm(self.sheepDog.coords - self.sheepGroup.coords.mean(axis=0))

    def step(self, sheepDog_coords=None):
        # todo 重写

        done = False

        # Model 0 represent the auto control for the sheepdog
        # Model 1 represent the mouse control for the sheepdog
        # action sheepdog
        if self.Model == 0:
            sheepDog_coords, self.kwargs = self.sheepDog.action(self.sheepGroup.coords)
        if self.Model == 1:
            _, self.kwargs = self.sheepDog.action(self.sheepGroup.coords)
            self.sheepDog.coords = sheepDog_coords


        # action sheepgroup
        sheepGroup_coords = self.sheepGroup.action(sheepDog_coords)

        GCM = self.sheepDog.getGCM(sheepGroup_coords)
        if self.isGetData:
            self.dogTrace.append(np.array(np.squeeze(sheepDog_coords)))
            if np.linalg.norm(sheepDog_coords - GCM) < self.sheepGroup.r_s:
                _, fur = SheepDog.getFurthestSheep(GCM, self.sheepGroup.coords)
                self.fur.append(np.round(fur))

        if np.linalg.norm(GCM - self.target) < self.sheepDog.r_a:
            done = True

        return done

    def reset(self):

        self.coordsInit()
        # if self.test_SheepGroup_coords is None:
        #     sheepGroup_coords = np.random.uniform(0, 1, [self.n_sheep, 2]) * self.WIN_HEIGHT / 7 + rand
        #     self.sheepGroup = SheepGroup(sheepGroup_coords, self.r_a, r_s=self.SheepGroup_info['r_s'],
        #                                  speed=self.SheepGroup_info['speed'], onNoise=self.onNoise)
        # else:
        #     self.sheepGroup = SheepGroup(self.test_SheepGroup_coords, self.r_a, r_s=self.SheepGroup_info['r_s'],
        #                                  speed=self.SheepGroup_info['speed'], onNoise=self.onNoise)
        #
        # if self.test_SheepDog_coords is None:
        #     sheepDog_coords = np.array([self.WIN_WIGHT - 50, self.WIN_HEIGHT - 50], dtype=np.float64).reshape(
        #         self.n_dog, 2)
        #     self.sheepDog = SheepDog(sheepDog_coords, self.sheepGroup.coords, self.target, r_a=self.r_a, fN=self.fN,
        #                              speed=self.SheepDog_info['speed'], onNoise=self.onNoise)
        # else:
        #     self.sheepDog = SheepDog(self.test_SheepDog_coords, self.sheepGroup.coords, self.target, r_a=self.r_a,
        #                              fN=self.fN, speed=self.SheepDog_info['speed'], onNoise=self.onNoise)

        if self.isGetData:
            self.dogTrace = []
            self.dogTrace.append(np.array(self.sheepDog.coords))
            self.fur = []
            self.initDistance = np.linalg.norm(self.sheepDog.coords - self.sheepGroup.coords.mean(axis=0))

    def getData(self):
        if self.isGetData:
            Data = {}
            Data['initDistance'] = self.initDistance
            Data['dogTrace'] = self.dogTrace
            Data['fur'] = self.fur
            return Data

    def coordsInit(self, test_SheepGroup_coords=None, test_SheepDog_coords=None):
        if self.isRandom:
            rand = np.random.randint(int(self.WIN_WIGHT / 7), self.WIN_HEIGHT - int(self.WIN_HEIGHT / 7))
        else:
            rand = 200

        if self.sheepGroupInitState == 0:

            if test_SheepGroup_coords is None:
                sheepGroup_coords = np.random.uniform(0, 1,
                                                      [self.n_sheep,
                                                       2]) * self.WIN_HEIGHT / 7 + rand  # initial sheep coords
                self.sheepGroup = SheepGroup(sheepGroup_coords, self.r_a, r_s=self.SheepGroup_info['r_s'],
                                             speed=self.SheepGroup_info['speed'], onNoise=self.onNoise)
            else:
                self.test_SheepGroup_coords = test_SheepGroup_coords
                self.sheepGroup = SheepGroup(self.test_SheepGroup_coords, self.r_a, r_s=self.SheepGroup_info['r_s'],
                                             speed=self.SheepGroup_info['speed'], onNoise=self.onNoise)
            if test_SheepDog_coords is None:
                sheepDog_coords = np.array([self.WIN_WIGHT - 50, self.WIN_HEIGHT - 50],
                                           dtype=np.float64).reshape(self.n_dog, 2)
                self.sheepDog = SheepDog(sheepDog_coords, self.sheepGroup.coords, self.target, r_a=self.r_a, fN=self.fN,
                                         speed=self.SheepDog_info['speed'], onNoise=self.onNoise)
            else:
                self.test_SheepDog_coords = test_SheepDog_coords
                self.sheepDog = SheepDog(self.test_SheepDog_coords, self.sheepGroup.coords, self.target, r_a=self.r_a,
                                         fN=self.fN, speed=self.SheepDog_info['speed'], onNoise=self.onNoise)

        if self.sheepGroupInitState == 1:
            sheepGroup_coords = abs(np.random.standard_normal([self.n_sheep, 2])) * self.WIN_HEIGHT / 7 + rand
            self.sheepGroup = SheepGroup(sheepGroup_coords, self.r_a, r_s=self.SheepGroup_info['r_s'],
                                         speed=self.SheepGroup_info['speed'], onNoise=self.onNoise)

            sheepDog_coords = np.array([self.WIN_WIGHT - 50, self.WIN_HEIGHT - 50],
                                       dtype=np.float64).reshape(self.n_dog, 2)
            self.sheepDog = SheepDog(sheepDog_coords, self.sheepGroup.coords, self.target, r_a=self.r_a, fN=self.fN,
                                     speed=self.SheepDog_info['speed'], onNoise=self.onNoise)


