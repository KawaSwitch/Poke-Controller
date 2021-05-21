#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os

from pynput.keyboard import Key, Listener
from logging import getLogger, DEBUG, NullHandler

from Commands.Keys import Button, Direction


# import logging


# This handles keyboard interactions
class Keyboard:
    def __init__(self):
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.listener = Listener(
            on_press=self.on_press,
            on_release=self.on_release)

    def listen(self):
        self.listener.start()
        self._logger.debug('Keyboard control start')

    def stop(self):
        self.listener.stop()
        self._logger.debug('Keyboard control stop')

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(self, key):
        print('{0} released'.format(key))


# This regards a keyboard inputs as Switch controller
class SwitchKeyboardController(Keyboard):
    SETTING_PATH = os.path.join(os.path.dirname(__file__), "settings.ini")

    def __init__(self, keyPress):
        super(SwitchKeyboardController, self).__init__()

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.to_use = Button.A
        self.setting = configparser.ConfigParser()
        self.setting.optionxform = str

        self._logger.debug('Loading Keyboard control key-map setting')
        if os.path.isfile(self.SETTING_PATH):
            self.setting.read(self.SETTING_PATH, encoding='utf-8')
        self.key = keyPress
        self.holding = []
        self.holdingDir = []
        self.key_map = {(i[1] if len(i[1]) == 1 else eval(str(i[1]))): eval(i[0]) for i in
                        self.setting.items("Key map")}
        # logging.error(self.key_map)

        self._logger.debug('Initialization finished')

    def on_press(self, key):
        # for debug (show row key data)
        # super().on_press(key)

        if key is None:
            print('unknown key has input')
            self._logger.warning('Unknown key has input')

        try:
            if key.char in self.holding:
                return

            for k in self.key_map.keys():
                if key.char == k:
                    self.key.input(self.key_map[key.char])
                    self.holding.append(key.char)
                    # self._logger.debug(f"push in {key.char}")

        # for special keys
        except AttributeError:
            if key in self.holdingDir:
                return

            for k in self.key_map.keys():
                if key == k:
                    self.holdingDir.append(key)
                    self.inputDir(self.holdingDir)
                    # self._logger.debug(f"stick: {key}")

    def on_release(self, key):
        if key is None:
            print('unknown key has released')
            self._logger.warning('Unknown key has input')

        try:
            if key.char in self.holding:
                self.holding.remove(key.char)
                # self._logger.debug("try")
                self.key.inputEnd(self.key_map[key.char])
                # self._logger.debug("done")
                # self._logger.debug(f"push out {self.key_map[key.char]}")

        except AttributeError:
            if key in self.holdingDir:
                self.holdingDir.remove(key)
                if self.holdingDir == []:
                    self.key.inputEnd(self.key_map[key])
                    # self._logger.debug(f"holding {self.holdingDir}")
                self.inputDir(self.holdingDir)

    def inputDir(self, dirs):
        if len(dirs) == 0:
            return
        elif len(dirs) == 1:
            self.key.input(self.key_map[dirs[0]])
        elif len(dirs) > 1:
            valid_dirs = dirs[-2:]  # set only last 2 directions

            if Key.up in valid_dirs:
                if Key.right in valid_dirs:
                    self.key.input(Direction.UP_RIGHT)
                elif Key.left in valid_dirs:
                    self.key.input(Direction.UP_LEFT)
            elif Key.down in valid_dirs:
                if Key.left in valid_dirs:
                    self.key.input(Direction.DOWN_LEFT)
                elif Key.right in valid_dirs:
                    self.key.input(Direction.DOWN_RIGHT)
