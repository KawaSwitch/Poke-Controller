#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick
import math
import numpy as np


# スティックの動作サンプルコード
class Stick_Sample2(PythonCommand):
	NAME = 'スティック2'

	def __init__(self):
		super().__init__()

	# press button at duration times(s)
	def stick(self, buttons, duration=0.1, wait=0.1):
		self.keys.input(buttons, ifPrint=False)
		self.wait(duration)
		self.wait(wait)
		self.checkIfAlive()

	# press button at duration times(s)
	def stickEnd(self, buttons):
		self.keys.inputEnd(buttons)
		self.checkIfAlive()

	def do(self):
		sin = np.empty(90)
		for i in range(0, 90):
			sin[i] = np.rad2deg(np.arcsin(i / 90))
		print(sin)
		sin2 = sin + 90
		sin3 = sin + 180
		sin4 = sin + 270
		sin = np.concatenate([sin, sin2, sin3, sin4])
		# print(sin)

		while True:
			angle = 0
			i = 0
			while True:
				angle_ = np.deg2rad(sin[(angle % 360)])
				if 0 <= angle_ < np.pi / 4 or np.pi * 7 / 4 <= angle_ < 2 * np.pi:
					r = np.sqrt(1 / 2 + ((1 / np.sqrt(2)) * np.tan(np.abs(np.pi * 0 / 2 - angle_))) ** 2)
				elif np.pi * 1 / 4 <= angle_ < np.pi * 3 / 4:
					r = np.sqrt(1 / 2 + ((1 / np.sqrt(2)) * np.tan(np.abs(np.pi * 1 / 2 - angle_))) ** 2)
				elif np.pi * 3 / 4 <= angle_ < np.pi * 5 / 4:
					r = np.sqrt(1 / 2 + ((1 / np.sqrt(2)) * np.tan(np.abs(np.pi * 2 / 2 - angle_))) ** 2)
				elif np.pi * 5 / 4 <= angle_ < np.pi * 7 / 4:
					r = np.sqrt(1 / 2 + ((1 / np.sqrt(2)) * np.tan(np.abs(np.pi * 3 / 2 - angle_))) ** 2)

				self.stick(Direction(Stick.LEFT, sin[(angle % 360)] + 45, r, showName='UP'), duration=0.00, wait=0.0)
				angle += 5
				i += 1
			self.wait(1.0)
			self.stickEnd(Direction(Stick.LEFT, i, i / 360, showName='UP'))
			self.press(Direction.DOWN, wait=0.5)
			self.wait(0.5)
			self.press(Button.A)
