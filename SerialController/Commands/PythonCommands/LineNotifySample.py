#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand
from LineNotify import Line_Notify


class LineSample(PythonCommand):
    NAME = 'LINE通知サンプル'

    def __init__(self):
        super().__init__()
        self.Line = Line_Notify(token_name="Another_token")

    def do(self):
        self.LINE_text("これはLINE通知のサンプルプログラムです")
