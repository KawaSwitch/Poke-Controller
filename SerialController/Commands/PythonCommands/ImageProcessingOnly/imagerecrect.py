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
        for i in range(1):
            result = self.isContainTemplate("shiny_mark.png", 0.7, show_value=True,
                                            show_position=True,  # このオプションをFalseにすると枠が非表示になります
                                            show_only_true_rect=True,  # このオプションをFalseにすると、
                                            # 認識できなかった場合に最も近い部分に赤枠を表示します
                                            ms=1000  # 枠の表示時間(ミリ秒)  デフォルトは2000msです
                                            )
            # self.wait(1)
