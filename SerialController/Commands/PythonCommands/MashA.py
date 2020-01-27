#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import PythonCommandBase as base

# Mash a button A
# A連打
class Mash_A(base.PythonCommand):
	NAME = 'A連打'

	def __init__(self, name):
		super(Mash_A, self).__init__(name)

	def do(self):
		while True:
			self.wait(0.5)
			self.press(Button.A)
