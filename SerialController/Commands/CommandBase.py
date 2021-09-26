#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
from . import Sender

class Command:
	__metaclass__ = ABCMeta

	def __init__(self):
		self.isRunning = False

	@abstractclassmethod
	def start(self, ser, postProcess=None):
		pass

	@abstractclassmethod
	def end(self, ser):
		pass

	def startWithOption(self, root, ser, postProcess=None):
		if self.openOptionDialog(root):
			self.apply()
			self.start(ser, postProcess)
			return True
		else:
			return False

	def openOptionDialog(self, root):
		return True

	def apply(self):
		pass