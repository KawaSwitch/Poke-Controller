#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import time
from collections import OrderedDict
from enum import Enum, IntEnum, IntFlag, auto
import queue
from logging import getLogger, DEBUG, NullHandler


class Button(IntFlag):
    Y = auto()
    B = auto()
    A = auto()
    X = auto()
    L = auto()
    R = auto()
    ZL = auto()
    ZR = auto()
    MINUS = auto()
    PLUS = auto()
    LCLICK = auto()
    RCLICK = auto()
    HOME = auto()
    CAPTURE = auto()


class Hat(IntEnum):
    TOP = 0
    TOP_RIGHT = 1
    RIGHT = 2
    BTM_RIGHT = 3
    BTM = 4
    BTM_LEFT = 5
    LEFT = 6
    TOP_LEFT = 7
    CENTER = 8


class Stick(Enum):
    LEFT = auto()
    RIGHT = auto()


class Tilt(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    R_UP = auto()
    R_RIGHT = auto()
    R_DOWN = auto()
    R_LEFT = auto()


# direction value definitions
min = 0
center = 128
max = 255


# serial format
class SendFormat:
    def __init__(self):

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        # This format structure needs to be the same as the one written in Joystick.c
        self.format = OrderedDict([
            ('btn', 0),  # send bit array for buttons
            ('hat', Hat.CENTER),
            ('lx', center),
            ('ly', center),
            ('rx', center),
            ('ry', center),
        ])

        self.L_stick_changed = False
        self.R_stick_changed = False
        self.Hat_pos = Hat.CENTER

    def setButton(self, btns):
        for btn in btns:
            self.format['btn'] |= btn

    def unsetButton(self, btns):
        for btn in btns:
            self.format['btn'] &= ~btn

    def resetAllButtons(self):
        self.format['btn'] = 0

    def setHat(self, btns):
        # self._logger.debug(btns)
        if not btns:
            self.format['hat'] = self.Hat_pos
        else:
            self.Hat_pos = btns[0]
            self.format['hat'] = btns[0]  # takes only first element

    def unsetHat(self):
        # if self.Hat_pos is not Hat.CENTER:
        self.Hat_pos = Hat.CENTER
        self.format['hat'] = self.Hat_pos

    def setAnyDirection(self, dirs):
        for dir in dirs:
            if dir.stick == Stick.LEFT:
                if self.format['lx'] != dir.x or self.format['ly'] != 255 - dir.y:
                    self.L_stick_changed = True

                self.format['lx'] = dir.x
                self.format['ly'] = 255 - dir.y  # NOTE: y axis directs under
            elif dir.stick == Stick.RIGHT:
                if self.format['rx'] != dir.x or self.format['ry'] != 255 - dir.y:
                    self.R_stick_changed = True

                self.format['rx'] = dir.x
                self.format['ry'] = 255 - dir.y

    def unsetDirection(self, dirs):
        if Tilt.UP in dirs or Tilt.DOWN in dirs:
            self.format['ly'] = center
            self.format['lx'] = self.fixOtherAxis(self.format['lx'])
            self.L_stick_changed = True
        if Tilt.RIGHT in dirs or Tilt.LEFT in dirs:
            self.format['lx'] = center
            self.format['ly'] = self.fixOtherAxis(self.format['ly'])
            self.L_stick_changed = True
        if Tilt.R_UP in dirs or Tilt.R_DOWN in dirs:
            self.format['ry'] = center
            self.format['rx'] = self.fixOtherAxis(self.format['rx'])
            self.R_stick_changed = True
        if Tilt.R_RIGHT in dirs or Tilt.R_LEFT in dirs:
            self.format['rx'] = center
            self.format['ry'] = self.fixOtherAxis(self.format['ry'])
            self.R_stick_changed = True

    # Use this to fix an either tilt to max when the other axis sets to 0
    def fixOtherAxis(self, fix_target):
        if fix_target == center:
            return center
        else:
            return 0 if fix_target < center else 255

    def resetAllDirections(self):
        self.format['lx'] = center
        self.format['ly'] = center
        self.format['rx'] = center
        self.format['ry'] = center
        self.L_stick_changed = True
        self.R_stick_changed = True
        self.Hat_pos = Hat.CENTER

    def convert2str(self):
        str_format = ''
        str_L = ''
        str_R = ''
        str_Hat = ''
        space = ' '

        # set bits array with stick flags
        send_btn = int(self.format['btn']) << 2
        if self.L_stick_changed:
            send_btn |= 0x2
            str_L = format(self.format['lx'], 'x') + space + format(self.format['ly'], 'x')
        if self.R_stick_changed:
            send_btn |= 0x1
            str_R = format(self.format['rx'], 'x') + space + format(self.format['ry'], 'x')
        # if self.Hat_changed:
        str_Hat = str(int(self.format['hat']))
        # format(send_btn, 'x') + \
        # print(hex(send_btn))
        str_format = format(send_btn, '#06x') + \
                     (space + str_Hat) + \
                     (space + str_L if self.L_stick_changed else ' 80 80') + \
                     (space + str_R if self.R_stick_changed else ' 80 80')

        self.L_stick_changed = False
        self.R_stick_changed = False

        # print(str_format)
        return str_format  # the last space is not needed


# This class handle L stick and R stick at any angles
class Direction:
    def __init__(self, stick, angle, magnification=1.0, isDegree=True, showName=None):

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.stick = stick
        self.angle_for_show = angle
        self.showName = showName
        if magnification > 1.0:
            self.mag = 1.0
        elif magnification < 0:
            self.mag = 0.0
        else:
            self.mag = magnification

        if isinstance(angle, tuple):
            # assuming (X, Y)
            self.x = angle[0]
            self.y = angle[1]
            self.showName = '(' + str(self.x) + ', ' + str(self.y) + ')'
            print('押し込み量', self.showName)
        else:
            angle = math.radians(angle) if isDegree else angle

            # We set stick X and Y from 0 to 255, so they are calculated as below.
            # X = 127.5*cos(theta) + 127.5
            # Y = 127.5*sin(theta) + 127.5
            self.x = math.ceil(127.5 * math.cos(angle) * self.mag + 127.5)
            self.y = math.floor(127.5 * math.sin(angle) * self.mag + 127.5)

    def __repr__(self):
        if self.showName:
            return "<{}, {}>".format(self.stick, self.showName)
        else:
            return "<{}, {}[deg]>".format(self.stick, self.angle_for_show)

    def __eq__(self, other):
        if not type(other) is Direction:
            return False

        if self.stick == other.stick and self.angle_for_show == other.angle_for_show:
            return True
        else:
            return False

    def getTilting(self):
        tilting = []
        if self.stick == Stick.LEFT:
            if self.x < center:
                tilting.append(Tilt.LEFT)
            elif self.x > center:
                tilting.append(Tilt.RIGHT)

            if self.y < center - 1:
                tilting.append(Tilt.DOWN)
            elif self.y > center - 1:
                tilting.append(Tilt.UP)
        elif self.stick == Stick.RIGHT:
            if self.x < center:
                tilting.append(Tilt.R_LEFT)
            elif self.x > center:
                tilting.append(Tilt.R_RIGHT)

            if self.y < center - 1:
                tilting.append(Tilt.R_DOWN)
            elif self.y > center - 1:
                tilting.append(Tilt.R_UP)
        return tilting


# Left stick for ease of use
Direction.UP = Direction(Stick.LEFT, 90, showName='UP')
Direction.RIGHT = Direction(Stick.LEFT, 0, showName='RIGHT')
Direction.DOWN = Direction(Stick.LEFT, -90, showName='DOWN')
Direction.LEFT = Direction(Stick.LEFT, -180, showName='LEFT')
Direction.UP_RIGHT = Direction(Stick.LEFT, 45, showName='UP_RIGHT')
Direction.DOWN_RIGHT = Direction(Stick.LEFT, -45, showName='DOWN_RIGHT')
Direction.DOWN_LEFT = Direction(Stick.LEFT, -135, showName='DOWN_LEFT')
Direction.DOWN_LEFT = Direction(Stick.LEFT, -135, showName='DOWN_LEFT')
Direction.UP_LEFT = Direction(Stick.LEFT, 135, showName='UP_LEFT')
# Right stick for ease of use
Direction.R_UP = Direction(Stick.RIGHT, 90, showName='UP')
Direction.R_RIGHT = Direction(Stick.RIGHT, 0, showName='RIGHT')
Direction.R_DOWN = Direction(Stick.RIGHT, -90, showName='DOWN')
Direction.R_LEFT = Direction(Stick.RIGHT, -180, showName='LEFT')
Direction.R_UP_RIGHT = Direction(Stick.RIGHT, 45, showName='UP_RIGHT')
Direction.R_DOWN_RIGHT = Direction(Stick.RIGHT, -45, showName='DOWN_RIGHT')
Direction.R_DOWN_LEFT = Direction(Stick.RIGHT, -135, showName='DOWN_LEFT')
Direction.R_UP_LEFT = Direction(Stick.RIGHT, 135, showName='UP_LEFT')


# handles serial input to Joystick.c
class KeyPress:
    def __init__(self, ser):

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.q = queue.Queue()
        self.ser = ser
        self.format = SendFormat()
        self.holdButton = []
        self.btn_name2 = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'UP_LEFT', 'UP_RIGHT', 'DOWN_LEFT', 'DOWN_RIGHT']

        self.pushing_to_show = None
        self.pushing = None
        self.pushing2 = None
        self._pushing = None
        self._chk_neutral = None
        self.NEUTRAL = dict(self.format.format)

        self.input_time_0 = time.perf_counter()
        self.input_time_1 = time.perf_counter()
        self.inputEnd_time_0 = time.perf_counter()
        self.was_neutral = True

    def input(self, btns, ifPrint=True):
        self._pushing = dict(self.format.format)
        if not isinstance(btns, list):
            btns = [btns]

        for btn in self.holdButton:
            if not btn in btns:
                btns.append(btn)

        self.format.setButton([btn for btn in btns if type(btn) is Button])
        self.format.setHat([btn for btn in btns if type(btn) is Hat])
        self.format.setAnyDirection([btn for btn in btns if type(btn) is Direction])

        self.ser.writeRow(self.format.convert2str())
        self.input_time_0 = time.perf_counter()

        # self._logger.debug(f": {list(map(str,self.format.format.values()))}")

    def inputEnd(self, btns, ifPrint=True, unset_hat=False):
        # self._logger.debug(f"input end: {btns}")
        self.pushing2 = dict(self.format.format)

        self.ed = time.perf_counter()
        if not isinstance(btns, list):
            btns = [btns]
        # self._logger.debug(btns)

        # get tilting direction from angles
        tilts = []
        for dir in [btn for btn in btns if type(btn) is Direction]:
            tiltings = dir.getTilting()
            for tilting in tiltings:
                tilts.append(tilting)
        # self._logger.debug(tilts)

        self.format.unsetButton([btn for btn in btns if type(btn) is Button])
        if unset_hat:
            self.format.unsetHat()
        self.format.unsetDirection(tilts)
        self.ser.writeRow(self.format.convert2str())

    def hold(self, btns):
        if not isinstance(btns, list):
            btns = [btns]

        for btn in btns:
            if btn in self.holdButton:
                print('Warning: ' + btn.name + ' is already in holding state')
                self._logger.warning(f"Warning: {btn.name} is already in holding state")
                return

            self.holdButton.append(btn)
        self.input(btns)

    def holdEnd(self, btns):
        if not isinstance(btns, list):
            btns = [btns]

        for btn in btns:
            self.holdButton.remove(btn)

        self.inputEnd(btns)

    def end(self):
        self.ser.writeRow('end')
