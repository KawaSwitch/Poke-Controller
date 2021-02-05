#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Stick
from Commands.PythonCommandBase import PythonCommand


# スティックの動作サンプルコード
class Stick_Sample1(PythonCommand):
    NAME = 'スティック1'

    def __init__(self):
        super().__init__()

    # press button at duration times(s)
    def stick(self, buttons, duration=0.1, wait=0.1):
        self.keys.input(buttons, ifPrint=False)
        # print(buttons)
        self.wait(duration)
        self.wait(wait)
        self.checkIfAlive()

    # press button at duration times(s)
    def stickEnd(self, buttons):
        self.keys.inputEnd(buttons)
        self.checkIfAlive()

    def do(self):
        while True:
            angle = 0
            i = 0
            while True:
                '''
                ここには動作サンプルコードを書く。スティック補正画面で挙動確認ができる。
                全体を通して極座標で考えていく。（角度と大きさで曲線をあらわす)
                
                なお、通常はself.press()を使うが、連続的にスティックを動かすとログが多すぎるので、self.stick()関数を作って使っている。
                
                angle : 角度(Degree)
                r :　スティックの傾き度合い(0<=r<=1.0)、1.0で傾き最大
                
                以下はr=0.5でangleを増加させながらstickを動かすコード
                50%位置をスティックが円形に移動する
                stickEnd()を行わないとスティックが入力されっぱなしになるので注意
                '''

                r = 0.5
                self.stick(Direction(Stick.LEFT, angle, r, showName=f'Angle={angle},r={r}'), duration=0.0, wait=0.0)
                angle += 5
                i += 1
            self.stickEnd(Direction(Stick.LEFT, i, i / 360, showName=f'Angle={angle},r={r}'))
