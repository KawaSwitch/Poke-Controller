#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import PythonCommandBase as base

# Auto league
# 自動リーグ周回(画像認識なし)
class AutoLeague(base.PythonCommand):
	def __init__(self, name):
		super(AutoLeague, self).__init__(name)

	def do(self):
		self.hold(Direction(Stick.LEFT, 70))
		while True:
			self.wait(0.5)

			for _ in range(0, 10):
				self.press(Button.A, wait=0.5)

			self.press(Button.B)
