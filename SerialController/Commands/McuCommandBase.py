#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CommandBase

# MCU command
class McuCommand(CommandBase.Command):
	def __init__(self, name, sync_name):
		super(McuCommand, self).__init__(name)
		#print('init MCU command: ' + name)
		self.sync_name = sync_name
		self.postProcess = None
	
	def start(self, ser, postProcess):
		ser.writeRow(self.sync_name)
		self.isRunning = True
		self.postProcess = postProcess

	def end(self, ser):
		ser.writeRow('end')
		self.isRunning = False
		if not self.postProcess is None:
			self.postProcess()
