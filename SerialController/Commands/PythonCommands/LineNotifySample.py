#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand
from Commands.PythonCommandBase import ImageProcPythonCommand


class LineSample(ImageProcPythonCommand):
    NAME = 'LINE通知サンプル'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.LINE_text("これはデフォルトのトークンへの通知")
        self.LINE_text("これは他のトークンへのテキスト通知", token='token_2')
        self.LINE_image("これは他のトークンへのテキスト+画像通知", token='token_2')
