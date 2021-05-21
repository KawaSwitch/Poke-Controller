#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand
from Commands.PythonCommandBase import ImageProcPythonCommand
from logging import getLogger, DEBUG, NullHandler


# ログ出力のサンプル
class LoggingSample(ImageProcPythonCommand):
    NAME = 'ログ出力のサンプル'

    def __init__(self, cam):
        super().__init__(cam)
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

    def do(self):
        self._logger.debug("DEBUG")
        self._logger.info("INFO")
        self._logger.warning("WARNING")
        self._logger.error("ERROR")
        self._logger.critical("CRITICAL")
