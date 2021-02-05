#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time

from Commands.PythonCommandBase import ImageProcPythonCommand


# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class CalcTime(ImageProcPythonCommand):
    NAME = 'テンプレートマッチング時間計測'

    def __init__(self, cam):
        super().__init__(cam)
        self.cam = cam

    def do(self):
        print(cv2.cuda.getCudaEnabledDeviceCount())

        iter = 1000
        # print(cv2.getBuildInformation())
        print("Measure Calc.Speed btw. CPU, GPU for {0} iter".format(iter))
        start = time.time()
        for i in range(iter):
            result = self.isContainTemplate("shiny_mark1.png", 0.7, True, False)
        n = time.time() - start
        print("CPU, Gray: Total: {0}, Ave: {1}".format(n, n / iter))
        start = time.time()
        for i in range(iter):
            result = self.isContainTemplate("shiny_mark1.png", 0.7, False, False)
        n = time.time() - start
        print("CPU, Color: Total: {0}, Ave: {1}".format(n, n / iter))

        start = time.time()
        for i in range(iter):
            result = self.isContainTemplateGPU("shiny_mark1.png", 0.7, True, False)
        n = time.time() - start
        print("GPU, Gray: Total: {0}, Ave: {1}".format(n, n / iter))
        start = time.time()
        for i in range(iter):
            result = self.isContainTemplateGPU("shiny_mark1.png", 0.7, False, False)
        n = time.time() - start
        print("GPU, Color: Total: {0}, Ave: {1}".format(n, n / iter))

# print("テンプレートマッチング　グレースケール")
# print("Total: {0}, Ave: {1}".format(n, n / 300))
# start = time.time()
# for i in range(300):
# 	self.isContainTemplate("shiny_mark.png", 0.8, False, False)
# n = time.time() - start
# print("テンプレートマッチング　カラー")
# print("Total: {0}, Ave: {1}".format(n, n / 300))
