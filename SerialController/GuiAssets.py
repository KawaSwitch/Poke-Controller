#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import numpy as np

from PIL import Image, ImageTk

from Commands import UnitCommand
from Commands import StickCommand
from Commands.Keys import Direction, Stick, Button, Direction, KeyPress

from logging import INFO, StreamHandler, getLogger, DEBUG
from Commands.PythonCommandBase import PythonCommand, StopThread

logger = getLogger(__name__)
handler = StreamHandler()
logging_level = INFO
handler.setLevel(logging_level)
logger.setLevel(logging_level)
logger.addHandler(handler)
logger.propagate = False


# press button at duration times(s)

class MouseStick(PythonCommand):
    NAME = 'スティック1'

    def __init__(self):
        super().__init__()

    def do(self):
        pass

    def stick(self, buttons, duration=0.1, wait=0.1):
        self.keys.input(buttons, ifPrint=False)
        self.wait(duration)
        self.wait(wait)

    # press button at duration times(s)
    def stickEnd(self, buttons):
        self.keys.inputEnd(buttons)


class CaptureArea(tk.Canvas):
    def __init__(self, camera, fps, is_show, ser, master=None, show_width=640, show_height=360):
        super().__init__(master, borderwidth=0, cursor='tcross', width=show_width, height=show_height)
        self.master = master
        self.radius = 60  # 描画する円の半径
        self.camera = camera
        # self.show_size = (640, 360)
        self.show_width = int(show_width)
        self.show_height = int(show_height)
        self.show_size = (self.show_width, self.show_height)
        self.is_show_var = is_show
        self.lx_init, self.ly_init = 0, 0
        self.rx_init, self.ry_init = 0, 0
        self.keys = None
        self.ser = ser
        self.circle = None
        # self.circle =

        self.setFps(fps)

        self.bind("<Control-ButtonPress-1>", self.mouseCtrlLeftPress)

        # Set disabled image first
        disabled_img = cv2.imread("../Images/disabled.png", cv2.IMREAD_GRAYSCALE)
        disabled_pil = Image.fromarray(disabled_img)
        self.disabled_tk = ImageTk.PhotoImage(disabled_pil)
        self.im = self.disabled_tk
        # self.configure(image=self.disabled_tk)  # labelからキャンバスに変更したので微修正
        self.im_ = self.create_image(0, 0, image=self.disabled_tk, anchor=tk.NW)

    def ApplyLStickMouse(self):
        if self.master.is_use_left_stick_mouse.get():
            self.bind("<ButtonPress-1>", self.mouseLeftPress)
            self.bind("<Button1-Motion>", lambda ev: self.mouseLeftPressing(ev, self.ser))
            self.bind("<ButtonRelease-1>", lambda ev: self.mouseLeftRelease(self.ser))
        else:
            self.unbind("<ButtonPress-1>")
            self.unbind("<Button1-Motion>")
            self.unbind("<ButtonRelease-1>")

    def ApplyRStickMouse(self):
        if self.master.is_use_right_stick_mouse.get():
            self.bind("<ButtonPress-3>", self.mouseRightPress)
            self.bind("<Button3-Motion>", lambda ev: self.mouseRightPressing(ev, self.ser))
            self.bind("<ButtonRelease-3>", lambda ev: self.mouseRightRelease(self.ser))
        else:
            self.unbind("<ButtonPress-3>")
            self.unbind("<Button3-Motion>")
            self.unbind("<ButtonRelease-3>")

    def setFps(self, fps):
        # self.next_frames = int(16 * (60 / int(fps)))
        self.next_frames = int(1000 / int(fps))

    def setShowsize(self, show_height, show_width):
        self.show_width = int(show_width)
        self.show_height = int(show_height)
        self.show_size = (self.show_width, self.show_height)
        self.config(width=self.show_width, height=self.show_height)
        print("Show size set to {0} x {1}".format(self.show_width, self.show_height))

    def mouseCtrlLeftPress(self, event):
        x, y = event.x, event.y
        ratio_x = float(self.camera.capture_size[0] / self.show_size[0])
        ratio_y = float(self.camera.capture_size[1] / self.show_size[1])
        print('mouse down: show ({}, {}) / capture ({}, {})'.format(x, y, int(x * ratio_x), int(y * ratio_y)))

    def mouseLeftPress(self, event):
        self.lx_init, self.ly_init = event.x, event.y

        self.circle = self.create_oval(self.lx_init - self.radius, self.ly_init - self.radius,
                                       self.lx_init + self.radius, self.ly_init + self.radius,
                                       outline='cyan', tag="lcircle")

    def mouseLeftPressing(self, event, ser, angle=0):
        langle = np.rad2deg(np.arctan2(self.ly_init - event.y, event.x - self.lx_init))
        mag = np.sqrt((self.ly_init - event.y) ** 2 + (event.x - self.lx_init) ** 2) / self.radius
        logger.debug(self.lx_init - event.x, self.ly_init - event.y, angle)
        StickCommand.StickLeft().start(ser, langle, r=mag)

    def mouseLeftRelease(self, ser):
        StickCommand.StickLeft().end(ser)
        self.delete("lcircle")

    def mouseRightPress(self, event):
        self.rx_init, self.ry_init = event.x, event.y

        self.circle = self.create_oval(self.rx_init - self.radius, self.ry_init - self.radius,
                                       self.rx_init + self.radius, self.ry_init + self.radius,
                                       outline='red', tag="rcircle")

    def mouseRightPressing(self, event, ser, angle=0):
        rangle = np.rad2deg(np.arctan2(self.ry_init - event.y, event.x - self.rx_init))
        mag = np.sqrt((self.ry_init - event.y) ** 2 + (event.x - self.rx_init) ** 2) / self.radius
        logger.debug(self.rx_init - event.x, self.ry_init - event.y, angle)
        StickCommand.StickRight().start(ser, rangle, r=mag)

    def mouseRightRelease(self, ser):
        StickCommand.StickRight().end(ser)
        self.delete("rcircle")

    def startCapture(self):
        self.capture()

    def capture(self):
        if self.is_show_var.get():
            image_bgr = self.camera.readFrame()
        else:
            self.after(self.next_frames, self.capture)
            return

        if image_bgr is not None:
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb).resize(self.show_size)
            image_tk = ImageTk.PhotoImage(image_pil)

            self.im = image_tk
            # self.configure( image=image_tk)
            self.itemconfig(self.im_, image=image_tk)
        else:
            self.im = self.disabled_tk
            # self.configure(image=self.disabled_tk)
            self.itemconfig(self.im_, image=self.disabled_tk)

        self.after(self.next_frames, self.capture)

    def saveCapture(self):
        self.camera.saveCapture()


# GUI of switch controller simulator
class ControllerGUI:
    def __init__(self, root, ser):
        self.window = tk.Toplevel(root)
        self.window.title('Switch Controller Simulator')
        self.window.geometry("%dx%d%+d%+d" % (600, 300, 250, 125))
        self.window.resizable(0, 0)

        joycon_L_color = '#95f1ff'
        joycon_R_color = '#ff6b6b'

        joycon_L_frame = tk.Frame(self.window, width=300, height=300, relief='flat', bg=joycon_L_color)
        joycon_R_frame = tk.Frame(self.window, width=300, height=300, relief='flat', bg=joycon_R_color)
        hat_frame = tk.Frame(joycon_L_frame, relief='flat', bg=joycon_L_color)
        abxy_frame = tk.Frame(joycon_R_frame, relief='flat', bg=joycon_R_color)

        # ABXY
        tk.Button(abxy_frame, text='A', command=lambda: UnitCommand.A().start(ser)).grid(row=1, column=2)
        tk.Button(abxy_frame, text='B', command=lambda: UnitCommand.B().start(ser)).grid(row=2, column=1)
        tk.Button(abxy_frame, text='X', command=lambda: UnitCommand.X().start(ser)).grid(row=0, column=1)
        tk.Button(abxy_frame, text='Y', command=lambda: UnitCommand.Y().start(ser)).grid(row=1, column=0)
        abxy_frame.place(relx=0.2, rely=0.3)

        # HAT
        tk.Button(hat_frame, text='UP', command=lambda: UnitCommand.UP().start(ser)).grid(row=0, column=1)
        tk.Button(hat_frame, text='', command=lambda: UnitCommand.UP_RIGHT().start(ser)).grid(row=0, column=2)
        tk.Button(hat_frame, text='RIGHT', command=lambda: UnitCommand.RIGHT().start(ser)).grid(row=1, column=2)
        tk.Button(hat_frame, text='', command=lambda: UnitCommand.DOWN_RIGHT().start(ser)).grid(row=2, column=2)
        tk.Button(hat_frame, text='DOWN', command=lambda: UnitCommand.DOWN().start(ser)).grid(row=2, column=1)
        tk.Button(hat_frame, text='', command=lambda: UnitCommand.DOWN_LEFT().start(ser)).grid(row=2, column=0)
        tk.Button(hat_frame, text='LEFT', command=lambda: UnitCommand.LEFT().start(ser)).grid(row=1, column=0)
        tk.Button(hat_frame, text='', command=lambda: UnitCommand.UP_LEFT().start(ser)).grid(row=0, column=0)
        hat_frame.place(relx=0.2, rely=0.6)

        # L side
        tk.Button(joycon_L_frame, text='L', width=20, command=lambda: UnitCommand.L().start(ser)).place(x=30, y=30)
        tk.Button(joycon_L_frame, text='ZL', width=20, command=lambda: UnitCommand.ZL().start(ser)).place(x=30, y=0)
        tk.Button(joycon_L_frame, text='LCLICK', width=7, command=lambda: UnitCommand.LCLICK().start(ser)).place(x=120,
                                                                                                                 y=120)
        tk.Button(joycon_L_frame, text='MINUS', width=5, command=lambda: UnitCommand.MINUS().start(ser)).place(x=220,
                                                                                                               y=70)
        tk.Button(joycon_L_frame, text='CAP', width=5, command=lambda: UnitCommand.CAPTURE().start(ser)).place(x=200,
                                                                                                               y=270)

        # R side
        tk.Button(joycon_R_frame, text='R', width=20, command=lambda: UnitCommand.R().start(ser)).place(x=120, y=30)
        tk.Button(joycon_R_frame, text='ZR', width=20, command=lambda: UnitCommand.ZR().start(ser)).place(x=120, y=0)
        tk.Button(joycon_R_frame, text='RCLICK', width=7, command=lambda: UnitCommand.RCLICK().start(ser)).place(x=120,
                                                                                                                 y=205)
        tk.Button(joycon_R_frame, text='PLUS', width=5, command=lambda: UnitCommand.PLUS().start(ser)).place(x=35, y=70)
        tk.Button(joycon_R_frame, text='HOME', width=5, command=lambda: UnitCommand.HOME().start(ser)).place(x=50,
                                                                                                             y=270)

        joycon_L_frame.grid(row=0, column=0)
        joycon_R_frame.grid(row=0, column=1)

        # button style settings
        for button in abxy_frame.winfo_children():
            self.applyButtonSetting(button)
        for button in hat_frame.winfo_children():
            self.applyButtonSetting(button)
        for button in [b for b in joycon_L_frame.winfo_children() if type(b) is tk.Button]:
            self.applyButtonColor(button)
        for button in [b for b in joycon_R_frame.winfo_children() if type(b) is tk.Button]:
            self.applyButtonColor(button)

    def applyButtonSetting(self, button):
        button['width'] = 7
        self.applyButtonColor(button)

    def applyButtonColor(self, button):
        button['bg'] = '#343434'
        button['fg'] = '#fff'

    def bind(self, event, func):
        self.window.bind(event, func)

    def protocol(self, event, func):
        self.window.protocol(event, func)

    def focus_force(self):
        self.window.focus_force()

    def destroy(self):
        self.window.destroy()


# To avoid the error says 'ScrolledText' object has no attribute 'flush'
class MyScrolledText(ScrolledText):
    def flush(self):
        pass
