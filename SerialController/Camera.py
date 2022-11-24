#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import datetime
import os
import numpy as np
from logging import getLogger, DEBUG, NullHandler


def imwrite(filename, img, params=None):
    _logger = getLogger(__name__)
    _logger.addHandler(NullHandler())
    _logger.setLevel(DEBUG)
    _logger.propagate = True
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        _logger.error(f"Image Write Error: {e}")
        return False


CAPTURE_DIR = "./Captures/"
def _get_save_filespec(filename: str) -> str:
    """
    画像ファイルの保存パスを取得する。

    入力が絶対パスの場合は、`CAPTURE_DIR`につなげずに返す。

    Args:
        filename (str): 保存名／保存パス

    Returns:
        str: _description_
    """
    if os.path.isabs(filename):
        return filename
    else:
        return os.path.join(CAPTURE_DIR, filename)


class Camera:
    def __init__(self, fps=45):
        self.camera = None
        self.capture_size = (1280, 720)
        # self.capture_size = (1920, 1080)
        self.capture_dir = "Captures"
        self.fps = int(fps)

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

    def openCamera(self, cameraId):
        if self.camera is not None and self.camera.isOpened():
            self._logger.debug("Camera is already opened")
            self.destroy()

        if os.name == 'nt':
            self._logger.debug("NT OS")
            self.camera = cv2.VideoCapture(cameraId, cv2.CAP_DSHOW)
        # self.camera = cv2.VideoCapture(cameraId)
        else:
            self._logger.debug("Not NT OS")
            self.camera = cv2.VideoCapture(cameraId)

        if not self.camera.isOpened():
            print("Camera ID " + str(cameraId) + " can't open.")
            self._logger.error(f"Camera ID {cameraId} cannot open.")
            return
        print("Camera ID " + str(cameraId) + " opened successfully")
        self._logger.debug(f"Camera ID {cameraId} opened successfully.")
        # print(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        # self.camera.set(cv2.CAP_PROP_FPS, 60)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_size[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_size[1])

    # self.camera.set(cv2.CAP_PROP_SETTINGS, 0)

    def isOpened(self):
        self._logger.debug("Camera is opened")
        return self.camera.isOpened()

    def readFrame(self):
        _, self.image_bgr = self.camera.read()
        return self.image_bgr

    def saveCapture(self, filename=None, crop=None, crop_ax=None, img=None):
        if crop_ax is None:
            crop_ax = [0, 0, 1280, 720]
        else:
            pass
            # print(crop_ax)

        dt_now = datetime.datetime.now()
        if filename is None or filename == "":
            filename = dt_now.strftime('%Y-%m-%d_%H-%M-%S') + ".png"
        else:
            filename = filename + ".png"

        if crop is None:
            image = self.image_bgr
        elif crop is 1 or crop is "1":
            image = self.image_bgr[
                    crop_ax[1]:crop_ax[3],
                    crop_ax[0]:crop_ax[2]
                    ]
        elif crop is 2 or crop is "2":
            image = self.image_bgr[
                    crop_ax[1]:crop_ax[1] + crop_ax[3],
                    crop_ax[0]:crop_ax[0] + crop_ax[2]
                    ]
        elif img is not None:
            image = img
        else:
            image = self.image_bgr

        if not os.path.exists(self.capture_dir):
            os.makedirs(self.capture_dir)
            self._logger.debug("Created Capture folder")

        save_path = _get_save_filespec(filename)

        try:
            imwrite(save_path, image)
            self._logger.debug(f"Capture succeeded: {save_path}")
            print('capture succeeded: ' + save_path)
        except cv2.error as e:
            print("Capture Failed")
            self._logger.error(f"Capture Failed :{e}")

    def destroy(self):
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()
            self.camera = None
            self._logger.debug("Camera destroyed")
