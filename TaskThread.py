# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 17:05
# @Author  : tanlei0
# @FileName: TaskThread.py

import threading

class TaskThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self.flag = 0



        




