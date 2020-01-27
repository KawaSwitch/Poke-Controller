#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import McuCommandBase.McuCommand

# Mash A button
class Mash_A(McuCommand):
	def __init__(self, name, sync_name = 'mash_a'):
		super(Mash_A, self).__init__(name, sync_name)
