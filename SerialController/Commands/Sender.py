#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import os
import time

import serial
from logging import getLogger, DEBUG, NullHandler


class Sender:
    def __init__(self, is_show_serial, if_print=True):
        self.ser = None
        self.is_show_serial = is_show_serial

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.before = None
        self.is_print = if_print
        self.time_bef = time.perf_counter()
        self.time_aft = time.perf_counter()
        self.Buttons = ["Stick.RIGHT", "Stick.LEFT",
                        "Button.Y", "Button.B", "Button.A", "Button.X",
                        "Button.L", "Button.R",
                        "Button.ZL", "Button.ZR",
                        "Button.MINUS", "Button.PLUS",
                        "Button.LCLICK", "Button.RCLICK",
                        "Button.HOME", "Button.CAPTURE", ]
        self.Hat = ["TOP", "TOP_RIGHT",
                    "RIGHT", "BTM_RIGHT",
                    "BTM", "BTM_LEFT",
                    "LEFT", "TOP_LEFT",
                    "CENTER"]

    def openSerial(self, portNum):
        try:
            if os.name == 'nt':
                print('connecting to ' + "COM" + str(portNum))
                self._logger.info('connecting to ' + "COM" + str(portNum))
                self.ser = serial.Serial("COM" + str(portNum), 9600)
                return True
            elif os.name == 'posix':
                print('connecting to ' + "/dev/ttyUSB" + str(portNum))
                self._logger.info('connecting to ' + "/dev/ttyUSB" + str(portNum))
                self.ser = serial.Serial("/dev/ttyUSB" + str(portNum), 9600)
                return True
            else:
                print('Not supported OS')
                self._logger.warning('Not supported OS')
                return False
        except IOError as e:
            print('COM Port: can\'t be established')
            self._logger.error('COM Port: can\'t be established')
            # print(e)
            return False

    def closeSerial(self):
        self._logger.debug("Closing the serial communication")
        self.ser.close()

    def isOpened(self):
        self._logger.debug("Checking if serial communication is open")
        return not self.ser is None and self.ser.isOpen()

    def writeRow(self, row):
        try:
            self.time_bef = time.perf_counter()
            if self.before is not None and self.before != 'end':
                output = self.before.split(' ')
                self.show_input(output)

            self.ser.write((row + '\r\n').encode('utf-8'))
            self.time_aft = time.perf_counter()
            self.before = row
        except serial.serialutil.SerialException as e:
            # print(e)
            self._logger.error(f"Error : {e}")
        except AttributeError as e:
            print('Using a port that is not open.')
            self._logger.error('Maybe Using a port that is not open.')
            self._logger.error(e)
        # self._logger.debug(f"{row}")
        # Show sending serial datas
        if self.is_show_serial.get():
            print(row)

    def show_input(self, output):
        # print(output)
        btns = [self.Buttons[x] for x in range(0, 16) if int(output[0], 16) >> x & 1]
        useRStick = int(output[0], 16) >> 0 & 1
        useLStick = int(output[0], 16) >> 1 & 1
        Hat = self.Hat[int(output[1])]
        if Hat is not "CENTER":
            btns = btns + ['Hat.' + str(Hat)]
        LStick = list(map(lambda x: int(x, 16), output[2:4]))
        RStick = list(map(lambda x: int(x, 16), output[4:]))
        LStick_deg = math.degrees(math.atan2(128 - LStick[1], LStick[0] - 128))
        RStick_deg = math.degrees(math.atan2(128 - RStick[1], RStick[0] - 128))
        if self.is_print:
            if len(btns) == 0:
                pass
            elif useLStick or useRStick:
                if LStick == [128, 128] and RStick == [128, 128]:
                    if len(btns) > 1:
                        print('self.press([{}, Direction({}, {:.0f})], '
                              'duration={:.2f})'.format(", ".join(btns[1:]), btns[0], LStick_deg,
                                                        self.time_bef - self.time_aft))
                        self._logger.debug('self.press([{}, Direction({}, {:.0f})], '
                                           'duration={:.2f})'.format(", ".join(btns[1:]), btns[0], LStick_deg,
                                                                     self.time_bef - self.time_aft))
                    elif len(btns) == 1:
                        pass
                elif LStick != [128, 128] and RStick == [128, 128]:
                    if len(btns) > 1:
                        print('self.press([{}, Direction({}, {:.0f})], '
                              'duration={:.2f})'.format(", ".join(btns[1:]), btns[0], LStick_deg,
                                                        self.time_bef - self.time_aft))
                        self._logger.debug('self.press([{}, Direction({}, {:.0f})], '
                                           'duration={:.2f})'.format(", ".join(btns[1:]), btns[0], LStick_deg,
                                                                     self.time_bef - self.time_aft))
                    elif len(btns) == 1:
                        print('self.press(Direction({}, {:.0f}), '
                              'duration={:.2f})'.format(btns[0], LStick_deg,
                                                        self.time_bef - self.time_aft))
                        self._logger.debug('self.press(Direction({}, {:.0f}), '
                                           'duration={:.2f})'.format(btns[0], LStick_deg,
                                                                     self.time_bef - self.time_aft))
                elif LStick == [128, 128] and RStick != [128, 128]:
                    if len(btns) > 1:
                        print('self.press([{}, Direction({}, {:.0f})], '
                              'duration={:.2f})'.format(", ".join(btns[1:]), btns[0], LStick_deg,
                                                        self.time_bef - self.time_aft))
                        self._logger.debug('self.press([{}, Direction({}, {:.0f})], '
                                           'duration={:.2f})'.format(", ".join(btns[1:]), btns[0], LStick_deg,
                                                                     self.time_bef - self.time_aft))
                    elif len(btns) == 1:
                        print('self.press(Direction({}, {:.0f}), '
                              'duration={:.2f})'.format(btns[0], LStick_deg,
                                                        self.time_bef - self.time_aft))
                        self._logger.debug('self.press(Direction({}, {:.0f}), '
                                           'duration={:.2f})'.format(btns[0], LStick_deg,
                                                                     self.time_bef - self.time_aft))
                elif LStick != [128, 128] and RStick != [128, 128]:
                    print('self.press([Direction({}, {:.0f}), '
                          'Direction({}, {:.0f})], duration={:.2f})'.format(btns[0], RStick_deg,
                                                                            btns[1], LStick_deg,
                                                                            self.time_bef - self.time_aft))
                    self._logger.debug('self.press([Direction({}, {:.0f}), '
                                       'Direction({}, {:.0f})], duration={:.2f})'.format(btns[0], RStick_deg,
                                                                                         btns[1], LStick_deg,
                                                                                         self.time_bef - self.time_aft))
            elif len(btns) == 1:
                print('self.press({}, duration={:.2f})'.format(btns[0],
                                                               self.time_bef - self.time_aft)
                      )
                self._logger.debug('self.press({}, duration={:.2f})'.format(btns[0],
                                                                            self.time_bef - self.time_aft)
                                   )
            elif len(btns) > 1:
                print('self.press([{}], duration={:.2f})'.format(", ".join(btns),
                                                                 self.time_bef - self.time_aft)
                      )
                self._logger.debug('self.press([{}], duration={:.2f})'.format(", ".join(btns),
                                                                              self.time_bef - self.time_aft)
                                   )
