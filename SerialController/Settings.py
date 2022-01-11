#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os
import tkinter as tk
from logging import getLogger, DEBUG, NullHandler


class GuiSettings:
    SETTING_PATH = os.path.join(os.path.dirname(__file__), "settings.ini")

    def __init__(self):

        self._logger = getLogger(__name__)
        self.setting = configparser.ConfigParser()
        self.setting.optionxform = str
        # print("isExistConfig =", os.path.exists(self.SETTING_PATH))

        if not os.path.exists(self.SETTING_PATH):
            self._logger.debug('Setting file does not exists.')
            self.generate()
            self.load()
            self._logger.debug('Settings file has been generated.')
        else:
            self._logger.debug('Setting file exists.')
            self.load()
            self._logger.debug('Settings file has been loaded.')

        # default
        self.camera_id = tk.IntVar(value=self.setting['General Setting'].getint('camera_id'))
        self.com_port = tk.IntVar(value=self.setting['General Setting'].getint('com_port'))
        self.com_port_name = tk.StringVar(value=self.setting['General Setting'].get('com_port_name'))
        self.fps = tk.StringVar(value=self.setting['General Setting']['fps'])
        self.show_size = tk.StringVar(value=self.setting['General Setting'].get('show_size'))
        self.is_show_realtime = tk.BooleanVar(value=self.setting['General Setting'].getboolean('is_show_realtime'))
        self.is_show_serial = tk.BooleanVar(value=self.setting['General Setting'].getboolean('is_show_serial'))
        self.is_use_keyboard = tk.BooleanVar(value=self.setting['General Setting'].getboolean('is_use_keyboard'))
        # Pokemon Home用の設定
        self.season = tk.StringVar(value=self.setting['Pokemon Home'].get('Season'))
        self.is_SingleBattle = tk.StringVar(value=self.setting['Pokemon Home'].get('Single or Double'))

    def load(self):
        if os.path.isfile(self.SETTING_PATH):
            self.setting.read(self.SETTING_PATH, encoding='utf-8')

    def generate(self):
        # logger.info('Create Default setting file.')
        # default
        self.setting['General Setting'] = {
            'camera_id': 0,
            'com_port': 0,
            'com_port_name': '',
            'fps': 45,
            'show_size': '640x360',
            'is_show_realtime': True,
            'is_show_serial': False,
            'is_use_keyboard': True,
        }
        # pokemon home用の設定
        self.setting['Pokemon Home'] = {
            'Season': 1,
            'Single or Double': 'シングル',
        }
        # keyconfig
        self.setting['KeyMap-Button'] = {
            'Button.Y': 'y',
            'Button.B': 'b',
            'Button.X': 'x',
            'Button.A': 'a',
            'Button.L': 'l',
            'Button.R': 'r',
            'Button.ZL': 'k',
            'Button.ZR': 'e',
            'Button.MINUS': 'm',
            'Button.PLUS': 'p',
            'Button.LCLICK': 'q',
            'Button.RCLICK': 'w',
            'Button.HOME': 'h',
            'Button.CAPTURE': 'c'}
        self.setting['KeyMap-Direction'] = {
            'Direction.UP': 'Key.up',
            'Direction.RIGHT': 'Key.right',
            'Direction.DOWN': 'Key.down',
            'Direction.LEFT': 'Key.left',
            'Direction.UP_RIGHT': '20001',
            'Direction.DOWN_RIGHT': '20002',
            'Direction.DOWN_LEFT': '20010',
            'Direction.UP_LEFT': '20011'
        }
        self.setting['KeyMap-Hat'] = {
            'Hat.TOP': '10000',
            "Hat.TOP_RIGHT": '10001',
            "Hat.RIGHT": '10010',
            "Hat.BTM_RIGHT": '10011',
            "Hat.BTM": '10100',
            "Hat.BTM_LEFT": '10101',
            "Hat.LEFT": '10110',
            "Hat.TOP_LEFT": '10111',
            "Hat.CENTER": '11000',
        }
        with open(self.SETTING_PATH, 'w', encoding='utf-8') as file:
            self.setting.write(file)
        os.chmod(path=self.SETTING_PATH, mode=0o777)

    def save(self, path=None):
        # Some preparations are needed because tkinter related objects are not serializable.

        self.setting['General Setting'] = {
            'camera_id': self.camera_id.get(),
            'com_port': self.com_port.get(),
            'com_port_name': self.com_port_name.get(),
            'fps': self.fps.get(),
            'show_size': self.show_size.get(),
            'is_show_realtime': self.is_show_realtime.get(),
            'is_show_serial': self.is_show_serial.get(),
            'is_use_keyboard': self.is_use_keyboard.get(),
        }
        # pokemon home用の設定
        self.setting['Pokemon Home'] = {
            'Season': self.season.get(),
            'Single or Double': self.is_SingleBattle.get(),
        }

        with open(self.SETTING_PATH, 'w', encoding='utf-8') as file:
            self.setting.write(file)
        os.chmod(path=self.SETTING_PATH, mode=0o777)
        self._logger.debug('Settings file has been saved.')
