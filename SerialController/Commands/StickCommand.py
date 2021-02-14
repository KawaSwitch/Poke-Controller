#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

from . import CommandBase
from .Keys import Button, Hat, KeyPress, Direction, Stick


# Sigle button command
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
    def stick(self, stick, duration=0.1, wait=0.1):
        self.key.input(stick, ifPrint=False)
        # print(buttons)
        self.wait(duration)
        self.wait(wait)

    def stick_end(self, stick=Direction(Stick.LEFT, 0)):
        self.key.inputEnd(stick)


class StickLeft(StickCommand):
    def __init__(self):
        super().__init__()

    def start(self, ser, angle, r=1.0):
        super().start(ser)
        self.stick(Direction(Stick.LEFT, angle, r, showName=f'Angle={angle},r={r}'), duration=0.015, wait=0.0)

    def end(self, ser):
        super().end(ser)
        self.stick_end(stick=Direction(Stick.LEFT, 0))


class StickRight(StickCommand):
    def __init__(self):
        super().__init__()

    def start(self, ser, angle, r=1.0):
        super().start(ser)
        self.stick(Direction(Stick.RIGHT, angle, r, showName=f'Angle={angle},r={r}'), duration=0.015, wait=0.0)

    def end(self, ser):
        super().end(ser)
        self.stick_end(stick=Direction(Stick.RIGHT, 0))
