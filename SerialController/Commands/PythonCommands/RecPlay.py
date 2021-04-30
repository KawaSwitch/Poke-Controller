#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Stick
from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand
from tkinter import filedialog
import time
import numpy as np


# Mash a button A
# A連打
class PlayRec(PythonCommand):
    NAME = '記録したログを再生'

    def __init__(self):
        super().__init__()

    # press button at duration times(s)
    def stick(self, buttons, duration=0.015, wait=0.1):
        self.keys.input(buttons, ifPrint=False)
        # print(buttons)
        time.sleep(duration)

    # press button at duration times(s)
    def stickEnd(self, buttons):
        self.keys.inputEnd(buttons)
        self.checkIfAlive()

    def LStick(self, angle, r=1.0, duration=0.015):
        self.keys.ser.writeRow(
            f'2 8 {hex(int(128 + r * 127.5 * np.cos(np.deg2rad(angle))))} {hex(int(128 - r * 127.5 * np.sin(np.deg2rad(angle))))}'
        )
        time.sleep(duration)

    def do(self):
        file = filedialog.askopenfile(initialdir='~/')
        self.log = file.name
        print(self.log)
        with open(self.log) as f:
            l_strip = [list(map(float, s.strip().split(","))) for s in f.readlines()]
            # print(l_strip[:20])
        for i in l_strip:
            self.LStick(i[0], i[1], duration=i[2] * 1.0)
            # self.wait(i[2]*0.90)

        self.stickEnd(Direction(Stick.LEFT, 0, 0, showName=f'Angle={l_strip[0][0]},r={l_strip[0][1]}'))
