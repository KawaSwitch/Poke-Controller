#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick
import GuiAssets
import tkinter as tk

class Hoge(PythonCommand):
	NAME = 'hoge'

	def __init__(self):
		super().__init__()

	def do(self):
		while True:
			self.wait(0.5)
			self.press(Button.A)

	def openOptionDialog(self, root):
		d = MyDialog(root, self.NAME)
		return d.option != None

	def apply(self):
		self.count = 0

class MyDialog(GuiAssets.Dialog):
	def __init__(self, parent, title = None):
		super().__init__(parent, title)

	def body(self, master):
		frame1, self.e1 = self.setLabelWithEntry(master, "First:")
		frame2, self.e2 = self.setLabelWithEntry(master, "Second:")
		frame1.grid(row=0)
		frame2.grid(row=1)

	def validate(self):
		try:
			first = int(self.e1.get())
			second = int(self.e2.get())
			self.option = first, second
			return 1
		except ValueError:
			tk.messagebox.showwarning("Input Value Error", "不正な入力値です.\nPlease try again.")
			return 0

	def apply(self):
		pass