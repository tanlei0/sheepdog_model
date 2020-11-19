# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 14:35
# @Author  : tanlei0
# @FileName: mouseMain.py

from Env2 import Env
import time
import pandas as pd
import numpy as np
import Viewer
import time
import pyglet
MAX_EPISODE = 8000
r_a = 10
r_s = 100

SheepGroup_para = {'r_a': r_a, 'r_s': r_s, 'n_sheep': 46, 'speed': 1}
SheepDog_para = {'n_dog': 1, 'speed': 1.5}

env = Env(SheepGroup_para, SheepDog_para, fN=60, isRandom=True, isGetData=False, onNoise=True, Model=1)

viewer = Viewer.Viewer(env.sheepGroup.coords, env.sheepDog.coords, env.target, env.WIN_WIGHT,
                       env.WIN_HEIGHT)


while True:
    mouseCoords = viewer.mouseCoords
    done = env.step(mouseCoords)
    time.sleep(0.01)
    if done:
        env.reset()

    viewer.render(env.sheepGroup.coords, env.sheepDog.coords, env.kwargs)

