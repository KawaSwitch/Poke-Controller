#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pynput.keyboard import Key, Listener
from Commands.Keys import KeyPress, Button, Direction, Stick

# This handles keyboard interactions
class Keyboard:
	def __init__(self):
		self.listener = Listener(
			on_press=self.on_press,
			on_release=self.on_release)
	
	def listen(self):
		self.listener.start()
	
	def stop(self):
		self.listener.stop()
	
	def on_press(self, key):
		try:
			print('alphanumeric key {0} pressed'.format(key.char))
		except AttributeError:
			print('special key {0} pressed'.format(key))

	def on_release(self, key):
		print('{0} released'.format(key))

# This regards a keyboard inputs as Switch controller
class SwitchKeyboardController(Keyboard):
	def __init__(self, keyPress):
		super(SwitchKeyboardController, self).__init__()
		self.key = keyPress
		self.holding = []

		self.key_map = {
			'y': Button.Y,
			'b': Button.B,
			'x': Button.X,
			'a': Button.A,
			'l': Button.L,
			'r': Button.R,
			'k': Button.ZL,
			'e': Button.ZR,
			'm': Button.MINUS,
			'p': Button.PLUS,
			'q': Button.LCLICK,
			'w': Button.RCLICK,
			'h': Button.HOME,
			'c': Button.CAPTURE,
			Key.up: Direction.UP,
			Key.right: Direction.RIGHT,
			Key.down: Direction.DOWN,
			Key.left: Direction.LEFT,
		}

	def on_press(self, key):
		# for debug (show row key data)
		#super().on_press(key)

		if key is None:
			print('unknown key has input')

		try:
			if key.char in self.holding:
				return

			for k in self.key_map.keys():
				if key.char == k:
					self.key.input(self.key_map[k])
					self.holding.append(key.char)
		
		# for special keys
		except AttributeError:
			if key in self.holding:
				return

			for k in self.key_map.keys():
				if key == k:
					self.key.input(self.key_map[k])
					self.holding.append(key)

			if Key.up in self.holding:
				if Key.right in self.holding:	self.key.input(Direction(Stick.LEFT, 45))
				elif Key.left in self.holding:	self.key.input(Direction(Stick.LEFT, 135))
			elif Key.down in self.holding:
				if Key.left in self.holding:	self.key.input(Direction(Stick.LEFT, 225))
				elif Key.right in self.holding:	self.key.input(Direction(Stick.LEFT, 315))

	def on_release(self, key):
		if key is None:
			print('unknown key has released')

		try:
			if key.char in self.holding:
				self.holding.remove(key.char)
				self.key.inputEnd(self.key_map[key.char])
		
		except AttributeError:
			if key in self.holding:
				self.holding.remove(key)
				self.key.inputEnd(self.key_map[key])