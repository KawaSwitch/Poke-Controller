#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import ImageProcPythonCommand


class ImageRecRect(ImageProcPythonCommand):
    NAME = '画像認識(枠表示)'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  # ← 必須の変更点です 引数が追加されています。
        self.cam = cam
        self.gui = gui  # この行はなくても動きますが一応

    def do(self):
        result = self.isContainTemplate("shiny_mark.png", 0.7, show_value=True
                                        # , show_position=False  #  このオプションをFalseで与えると枠非表示になります
                                        )
