#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

from . import CommandBase
import numpy as np
from .Keys import Button, Hat, KeyPress, Direction, Stick


# Single button command
class StickCommand(CommandBase.Command):
    def __init__(self):
        super().__init__()
        self.key = None

    def start(self, ser, postProcess=None):
        self.isRunning = True
        self.key = KeyPress(ser)

    def end(self, ser):
        self.isRunning = True
        self.key = KeyPress(ser)
        pass

    # do nothing at wait time(s)
    def wait(self, wait):
        sleep(wait)

    def press(self, btn):
        self.key.input([btn])
        self.wait(0.1)
        self.key.inputEnd([btn])
        self.isRunning = False
        self.key = None

    # press button at duration times(s)
    def stick(self, stick, duration=0.015, wait=0):
        self.key.input(stick, ifPrint=False)
        # print(buttons)
        self.wait(duration)
        self.wait(wait)

    def stick_end(self, stick=Direction(Stick.LEFT, 0)):
        self.key.inputEnd(stick)


class StickLeft(StickCommand):
    def __init__(self):
        super().__init__()

    def start(self, ser, postprocess=None):
        super().start(ser)
        self.key = KeyPress(ser)

    def LStick(self, angle, r=1.0, duration=0.015):
        self.key.ser.writeRow(
            f'2 8 {hex(int(128 + r * 127.5 * np.cos(np.deg2rad(angle))))} {hex(int(128 - r * 127.5 * np.sin(np.deg2rad(angle))))}'
        )
        # self.stick(Direction(Stick.LEFT, angle, r, showName=f'Angle={angle},r={r}'), duration=duration, wait=0)

    def end(self, ser):
        super().end(ser)
        self.stick_end(stick=Direction(Stick.LEFT, 0))


class StickRight(StickCommand):
    def __init__(self):
        super().__init__()

    def start(self, ser):
        super().start(ser)

    def RStick(self, angle, r=1.0, duration=0.015):
        self.key.ser.writeRow(
            f'1 8 {hex(int(128 + r * 127.5 * np.cos(np.deg2rad(angle))))} {hex(int(128 - r * 127.5 * np.sin(np.deg2rad(angle))))}'
        )

    def end(self, ser):
        super().end(ser)
        self.stick_end(stick=Direction(Stick.RIGHT, 0))
