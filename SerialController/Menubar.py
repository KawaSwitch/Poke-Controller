import tkinter as tk
import cv2
from LineNotify import Line_Notify


class PokeController_Menubar(tk.Menu):
	def __init__(self, master, **kw):
		self.master = master
		self.root = self.master.root
		self.ser = self.master.ser
		self.keyboard = self.master.keyboard
		self.settings = self.master.settings
		self.camera = self.master.camera

		tk.Menu.__init__(self, self.root, **kw)
		self.menu = tk.Menu(self, tearoff='false')
		self.menu_command = tk.Menu(self, tearoff='false')
		self.add(tk.CASCADE, menu=self.menu, label='メニュー')
		self.menu.add(tk.CASCADE, menu=self.menu_command, label='コマンド')

		self.menu.add('separator')
		self.menu.add('command', label='設定(dummy)')
		# TODO: setup command_id_arg 'false' for menuitem.
		self.menu.add('command', command=self.exit, label='終了')

		self.AssignMenuCommand()

	# TODO: setup command_id_arg 'false' for menuitem.

	def AssignMenuCommand(self):
		self.menu_command.add('command', command=self.LineTokenSetting, label='LINE 連携')
		# TODO: setup command_id_arg 'false' for menuitem.
		self.menu_command.add('command', command=self.OpenPokeHomeCoop, label='Pokemon Home 連携')
		# TODO: setup command_id_arg 'false' for menuitem.

	def OpenPokeHomeCoop(self, GUI):
		pass

	def LineTokenSetting(self):

		LINE = Line_Notify(self.camera)
		LINE.send_text_n_image("CAPTURE")

	def exit(self):
		if self.ser.isOpened():
			self.ser.closeSerial()
			print("serial disconnected")

		# stop listening to keyboard events
		if self.keyboard is not None:
			self.keyboard.stop()
			self.keyboard = None

		# save settings
		self.settings.save()

		self.camera.destroy()
		cv2.destroyAllWindows()
		self.master.destroy()


if __name__ == '__main__':
	root = tk.Tk()
	widget = PokeController_Menubar(root)
	widget.pack(expand=True, fill='both')
	root.mainloop()
