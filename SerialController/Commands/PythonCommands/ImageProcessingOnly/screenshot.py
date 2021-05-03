#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import ImageProcPythonCommand


class ScreenShot(ImageProcPythonCommand):
    NAME = 'スクショ取るだけ'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.camera.saveCapture()
        self.camera.saveCapture(filename="ファイル名指定")
        self.camera.saveCapture(filename="4座標指定", crop=1, crop_ax=[500, 300, 800, 500])
        self.camera.saveCapture(filename="始点+大きさ指定", crop=2, crop_ax=[500, 300, 300, 300])
