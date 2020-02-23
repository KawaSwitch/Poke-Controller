#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import cv2
from PIL import Image, ImageTk
from Commands import UnitCommand

class CaptureArea(tk.Label):
	def __init__(self, camera, fps, is_show, master=None):
		super().__init__(master, borderwidth=0, cursor='tcross')
		self.camera = camera
		self.show_size = (640, 360)
		self.is_show_var = is_show

		self.setFps(fps)
		self.bind("<ButtonPress-1>", self.mouseLeftDown)

		# Set disabled image first
		disabled_img = cv2.imread("../Images/disabled.png", cv2.IMREAD_GRAYSCALE)
		disabled_pil = Image.fromarray(disabled_img)
		self.diabled_tk = ImageTk.PhotoImage(disabled_pil)
		self.im = self.diabled_tk
		self.configure(image=self.diabled_tk)
	
	def setFps(self, fps):
		self.next_frames = (int)(16 * (60 / int(fps)))

	def mouseLeftDown(self, event):
		x, y = event.x, event.y
		ratio_x = float(self.camera.capture_size[0] / self.show_size[0])
		ratio_y = float(self.camera.capture_size[1] / self.show_size[1])
		print('mouse down: show ({}, {}) / capture ({}, {})'.format(x, y, int(x * ratio_x), int(y * ratio_y)))
	
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
			image_tk  = ImageTk.PhotoImage(image_pil)

			self.im = image_tk
			self.configure(image=image_tk)
		else:
			self.im = self.diabled_tk
			self.configure(image=self.diabled_tk)
		
		self.after(self.next_frames, self.capture)

	def saveCapture(self):
		self.camera.saveCapture()

# The modal dialog
# based from here: http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class Dialog(tk.Toplevel):
	def __init__(self, parent, title = None):
		tk.Toplevel.__init__(self, parent)
		self.transient(parent)
		self.option = None

		if title:
			self.title(title)

		self.parent = parent
		self.result = None

		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)

		self.setButtonbox()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx(),
								  parent.winfo_rooty()))

		self.initial_focus.focus_set()
		self.wait_window(self)

	# Create dialog body that returns widget that should have initial focus.  
	# This method should be overridden.
	def body(self, master):
		pass

	# Add standard button box. Override if you don't want the standard buttons.
	def setButtonbox(self):
		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	def ok(self, event=None):
		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()
		self.cancel()

	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	def validate(self):
		return 1 # override

	def apply(self):
		pass # override

	## -- Set syntax-sugars
	def setLabel(self, master, text):
		return tk.Label(master, text=text)
	
	def setLabelWithEntry(self, master, text):
		frame = tk.Frame(master, relief='flat')
		tk.Label(frame, text=text).grid(row=0, column=0)
		entry = tk.Entry(frame)
		entry.grid(row=0, column=1)
		return frame, entry
	
	def setSelectRadioButton(self, master, text, radio_pairs, init_var=0):
		frame = tk.Frame(master, relief='flat')
		tk.Label(frame, text=text).grid(row=0, column=0)
		
		var = tk.IntVar(value=0)
		for i, (k, text) in enumerate(radio_pairs.items()):
			tk.Radiobutton(frame, value=k, variable=var, text=text).grid(row=1, column=i)
		var.set(init_var)

		return frame, var

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
		# internal implements are not HAT buttons actually (just direction sticks), but we may change later
		tk.Button(hat_frame, text='UP', command=lambda: UnitCommand.UP().start(ser)).grid(row=0, column=1)
		tk.Button(hat_frame, text='RIGHT', command=lambda: UnitCommand.RIGHT().start(ser)).grid(row=1, column=2)
		tk.Button(hat_frame, text='DOWN', command=lambda: UnitCommand.DOWN().start(ser)).grid(row=2, column=1)
		tk.Button(hat_frame, text='LEFT', command=lambda: UnitCommand.LEFT().start(ser)).grid(row=1, column=0)
		hat_frame.place(relx=0.2, rely=0.6)

		# L side
		tk.Button(joycon_L_frame, text='L', width=20, command=lambda: UnitCommand.L().start(ser)).place(x=30, y=30)
		tk.Button(joycon_L_frame, text='ZL', width=20, command=lambda: UnitCommand.ZL().start(ser)).place(x=30, y=0)
		tk.Button(joycon_L_frame, text='LCLICK', width=7, command=lambda: UnitCommand.LCLICK().start(ser)).place(x=120, y=120)
		tk.Button(joycon_L_frame, text='MINUS', width=5, command=lambda: UnitCommand.MINUS().start(ser)).place(x=220, y=70)
		tk.Button(joycon_L_frame, text='CAP', width=5, command=lambda: UnitCommand.CAPTURE().start(ser)).place(x=200, y=270)

		# R side
		tk.Button(joycon_R_frame, text='R', width=20, command=lambda: UnitCommand.R().start(ser)).place(x=120, y=30)
		tk.Button(joycon_R_frame, text='ZR', width=20, command=lambda: UnitCommand.ZR().start(ser)).place(x=120, y=0)
		tk.Button(joycon_R_frame, text='RCLICK', width=7, command=lambda: UnitCommand.RCLICK().start(ser)).place(x=120, y=205)
		tk.Button(joycon_R_frame, text='PLUS', width=5, command=lambda: UnitCommand.PLUS().start(ser)).place(x=35, y=70)
		tk.Button(joycon_R_frame, text='HOME', width=5, command=lambda: UnitCommand.HOME().start(ser)).place(x=50, y=270)

		ttk.Label(self.window, text='or Keyboard can be used').place(x=450, y=270)

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