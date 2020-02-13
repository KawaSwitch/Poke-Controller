#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick
import GuiAssets

# auto releaseing pokemons
class AutoRelease(ImageProcPythonCommand):
	NAME = '自動リリース'

	def __init__(self, cam):
		super().__init__(cam)
		self.row = 5
		self.col = 6
		self.cam = cam

	def do(self):
		self.wait(0.5)

		for i in range(0, self.row):
			for j in range(0, self.col):
				if not self.cam.isOpened():
					self.Release()
				else:
					# if shiny, then skip
					if not self.isContainTemplate('shiny_mark.png', threshold=0.9):
						if self.isContainTemplate('status.png', threshold=0.7): # Maybe this threshold works for only Japanese version.
							# Release a pokemon
							self.Release()


				if not j == self.col - 1:
					if i % 2 == 0:	self.press(Direction.RIGHT, wait=0.2)
					else:			self.press(Direction.LEFT, wait=0.2)

			self.press(Direction.DOWN, wait=0.2)

		# Return from pokemon box
		self.press(Button.B, wait=2)
		self.press(Button.B, wait=2)
		self.press(Button.B, wait=1.5)

	def Release(self):
		self.press(Button.A, wait=0.5)
		self.press(Direction.UP, wait=0.2)
		self.press(Direction.UP, wait=0.2)
		self.press(Button.A, wait=1)
		self.press(Direction.UP, wait=0.2)
		self.press(Button.A, wait=1.5)
		self.press(Button.A, wait=0.3)
	
	def openOptionDialog(self, root):
		self.option = MyDialog(root, self.NAME).option
		return self.option != None

	def apply(self):
		print(self.option)

class MyDialog(GuiAssets.Dialog):
	def __init__(self, parent, title = None):
		super().__init__(parent, title)

	def body(self, master):
		frame, self.var = self.setSelectRadioButton(master, "画像認識", ["使用する", "使用しない", "テスト"])
		frame.grid(row=0)

	def validate(self):
		try:
			rb_var = self.var
			self.option = rb_var.get(), rb_var.get()
			return 1
		except ValueError:
			tk.messagebox.showwarning("Input Value Error", "不正な入力値です.\nPlease try again.")
			return 0

	def apply(self):
		pass