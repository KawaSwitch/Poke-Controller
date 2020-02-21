#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# reset the game
class Reset(PythonCommand):
	NAME = "Reset"

	def __init__(self):
		super().__init__()

	def do(self):
		self.wait(1)
		self.press(Button.HOME, wait=1)
		self.press(Button.X, wait=1)
		self.press(Button.A, wait=5)
		self.press(Button.A, wait=2)
		self.press(Button.A, wait=18)
		self.press(Button.A, wait=1)