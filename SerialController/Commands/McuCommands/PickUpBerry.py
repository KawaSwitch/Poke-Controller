#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.McuCommandBase import McuCommand


# Mash A button
class PickUpBerry(McuCommand):
    NAME = 'きのみ回収'

    def __init__(self, sync_name='pickupberry'):
        super().__init__(sync_name)
