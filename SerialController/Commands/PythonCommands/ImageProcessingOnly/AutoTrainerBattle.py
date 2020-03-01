#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# Battle through trainers by setting up with Swords Dance/X-Attack
# Spams the pokemon's slot 1 attack. Assumes swords dance is in slot 4
class AutoTrainerBattle(ImageProcPythonCommand):
	NAME = 'Auto Trainer Battle'

	def __init__(self, cam):
		super().__init__(cam)
		self.exit = False
		self.use_swords_dance = False
		self.times_set_up = 1
		self.before_battle = False
		self.after_battle = False

	def do(self):
		while True:
			text = self.getText()
			if "You are challenged by" in text:
				print("Entering Trainer battle...")
				self.before_battle = False
				self.after_battle = False
				if self.exit:
					return
				self.wait(20)
				self.press(Button.A)
			self.press(Button.B)