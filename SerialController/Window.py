import cv2
import os
import sys
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsg
from logging import StreamHandler, getLogger, DEBUG, NullHandler

from pygubu.widgets.scrollbarhelper import ScrollbarHelper

import Settings
import Utility as util
from Camera import Camera
from CommandLoader import CommandLoader
from Commands import McuCommandBase, PythonCommandBase, Sender
import PokeConLogger
from Commands.Keys import KeyPress
from GuiAssets import CaptureArea, ControllerGUI
from Keyboard import SwitchKeyboardController
from Menubar import PokeController_Menubar

# from get_pokestatistics import GetFromHomeGUI

NAME = "Poke-Controller"
VERSION = "v3.0.2.5 Modified"  # based on 1.0-beta3

'''
Todo:
・デバッグ用にPoke-Controller本体にコントローラーを接続して動かしたい

・keyboardからHatを動かせないから、Hatを動かせるようにしたい
→モンハンのメニューの選択はHatで選ばれる
---> Done

・画像認識の時の枠を設定でON/OFFできると嬉しい
'''


class PokeControllerApp:
    def __init__(self, master=None):

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())

        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.root = master
        self.root.title(NAME + ' ' + VERSION)
        # self.root.resizable(0, 0)
        self.controller = None
        self.poke_treeview = None
        self.keyPress = None
        self.keyboard = None

        '''
        ここから
        '''
        # build ui
        self.frame_1 = ttk.Frame(master)
        self.camera_lf = ttk.Labelframe(self.frame_1)
        self.label_1 = ttk.Label(self.camera_lf)
        self.label_1.config(anchor='center', text='Camera ID:')
        self.label_1.grid(padx='5', sticky='ew')
        self.camera_entry = ttk.Entry(self.camera_lf)
        self.camera_id = tk.IntVar()
        self.camera_entry.config(state='normal', textvariable=self.camera_id)
        self.camera_entry.grid(column='1', padx='5', row='0', sticky='ew')
        self.camera_entry.columnconfigure('1', uniform='0')
        self.reloadButton = ttk.Button(self.camera_lf)
        self.reloadButton.config(text='Reload Camera')
        self.reloadButton.grid(column='2', padx='5', row='0', sticky='ew')
        self.reloadButton.configure(command=self.openCamera)
        self.separator_1 = ttk.Separator(self.camera_lf)
        self.separator_1.config(orient='vertical')
        self.separator_1.grid(column='3', row='0', sticky='ns')
        self.cb1 = ttk.Checkbutton(self.camera_lf)
        self.is_show_realtime = tk.BooleanVar()
        self.cb1.config(text='Show Realtime', variable=self.is_show_realtime)
        self.cb1.grid(column='4', row='0')
        self.separator_2 = ttk.Separator(self.camera_lf)
        self.separator_2.config(orient='vertical')
        self.separator_2.grid(column='5', row='0', sticky='ns')
        self.captureButton = ttk.Button(self.camera_lf)
        self.captureButton.config(text='Capture')
        self.captureButton.grid(column='6', row='0')
        self.captureButton.configure(command=self.saveCapture)
        self.camera_f2 = ttk.Frame(self.camera_lf)
        self.label3 = ttk.Label(self.camera_f2)
        self.label3.config(text='FPS:')
        self.label3.grid(padx='5', sticky='ew')
        self.fps_cb = ttk.Combobox(self.camera_f2)
        self.fps = tk.StringVar()
        self.fps_cb.config(justify='right', state='readonly', textvariable=self.fps, values=[60, 45, 30, 15, 5])
        self.fps_cb.config(width='5')
        self.fps_cb.grid(column='1', padx='10', row='0', sticky='ew')
        self.fps_cb.bind('<<ComboboxSelected>>', self.applyFps, add='')
        self.separator_3 = ttk.Separator(self.camera_f2)
        self.separator_3.config(orient='vertical')
        self.separator_3.grid(column='2', row='0', sticky='ns')
        self.show_size_label = ttk.Label(self.camera_f2)
        self.show_size_label.config(text='Show Size:')
        self.show_size_label.grid(column='3', padx='5', row='0', sticky='ew')
        self.show_size_cb = ttk.Combobox(self.camera_f2)
        self.show_size = tk.StringVar()
        self.show_size_cb.config(textvariable=self.show_size, state='readonly', values='640x360 1280x720 1920x1080')
        self.show_size_cb.grid(column='4', padx='10', row='0', sticky='ew')
        self.show_size_cb.bind('<<ComboboxSelected>>', self.applyWindowSize, add='')
        self.camera_f2.grid(column='0', columnspan='7', row='3', sticky='nsew')
        self.camera_name_l = ttk.Label(self.camera_lf)
        self.camera_name_l.config(anchor='center', text='Camera Name: ')
        self.camera_name_l.grid(column='0', padx='5', row='1', sticky='ew')
        self.Camera_Name = ttk.Combobox(self.camera_lf)
        self.camera_name_fromDLL = tk.StringVar()
        self.Camera_Name.config(state='normal', textvariable=self.camera_name_fromDLL)
        self.Camera_Name.grid(column='1', columnspan='6', padx='5', row='1', sticky='ew')
        self.Camera_Name.bind('<<ComboboxSelected>>', self.set_cameraid, add='')
        self.frame_1_2 = ttk.Frame(self.camera_lf)
        self.frame_1_2.config(height='360', relief='groove', width='640')
        self.frame_1_2.grid(column='0', columnspan='7', row='2')
        self.camera_lf.config(height='200', text='Camera', width='200')
        self.camera_lf.grid(columnspan='3', padx='5', sticky='ew')
        self.serial_lf = ttk.Labelframe(self.frame_1)
        self.label2 = ttk.Label(self.serial_lf)
        self.label2.config(text='COM Port: ')
        self.label2.grid(padx='5', sticky='ew')
        self.label2.rowconfigure('0', uniform='None', weight='0')
        self.entry2 = ttk.Entry(self.serial_lf)
        self.com_port = tk.IntVar()
        self.entry2.config(textvariable=self.com_port, width='5')
        self.entry2.grid(column='1', padx='5', row='0', sticky='ew')
        self.entry2.rowconfigure('0', uniform='None', weight='0')
        self.reloadComPort = ttk.Button(self.serial_lf)
        self.reloadComPort.config(text='Reload Port')
        self.reloadComPort.grid(column='2', row='0')
        self.reloadComPort.rowconfigure('0', uniform='None', weight='0')
        self.reloadComPort.configure(command=self.activateSerial)
        self.separator_4 = ttk.Separator(self.serial_lf)
        self.separator_4.config(orient='vertical')
        self.separator_4.grid(column='3', padx='5', row='0', sticky='ns')
        self.separator_4.rowconfigure('0', uniform='None', weight='0')
        self.separator_4.columnconfigure('3', uniform='None', weight='0')
        self.checkbutton_2 = ttk.Checkbutton(self.serial_lf)
        self.is_show_serial = tk.BooleanVar()
        self.checkbutton_2.config(text='Show Serial', variable=self.is_show_serial)
        self.checkbutton_2.grid(column='4', columnspan='2', padx='5', row='0', sticky='ew')
        self.checkbutton_2.rowconfigure('0', uniform='None', weight='0')
        self.serial_lf.config(text='Serial Settings')
        self.serial_lf.grid(column='0', columnspan='2', padx='5', row='1', sticky='nsew')
        self.control_lf = ttk.Labelframe(self.frame_1)
        self.cb_use_keyboard = ttk.Checkbutton(self.control_lf)
        self.cb_left_stick_mouse = ttk.Checkbutton(self.control_lf)
        self.cb_right_stick_mouse = ttk.Checkbutton(self.control_lf)
        self.is_use_keyboard = tk.BooleanVar()
        self.camera_lf.is_use_left_stick_mouse = tk.BooleanVar()
        self.camera_lf.is_use_right_stick_mouse = tk.BooleanVar()
        self.cb_use_keyboard.config(text='Use Keyboard', variable=self.is_use_keyboard)
        self.cb_use_keyboard.grid(column='0', padx='10', pady='5', sticky='ew')
        self.cb_use_keyboard.rowconfigure('0', weight='1')
        self.cb_use_keyboard.columnconfigure('0', weight='1')
        self.cb_use_keyboard.configure(command=self.activateKeyboard)
        self.cb_left_stick_mouse.config(text='Use LStick Mouse', variable=self.camera_lf.is_use_left_stick_mouse)
        self.cb_left_stick_mouse.grid(column='1', row='0', padx='10', pady='5', sticky='ew')
        self.cb_left_stick_mouse.rowconfigure('0', weight='1')
        self.cb_left_stick_mouse.columnconfigure('0', weight='1')
        self.cb_left_stick_mouse.configure(command=self.activate_Left_stick_mouse)
        self.cb_right_stick_mouse.config(text='Use RStick Mouse', variable=self.camera_lf.is_use_right_stick_mouse)
        self.cb_right_stick_mouse.grid(column='1', row='1', padx='10', pady='5', sticky='ew')
        self.cb_right_stick_mouse.rowconfigure('0', weight='1')
        self.cb_right_stick_mouse.columnconfigure('0', weight='1')
        self.cb_right_stick_mouse.configure(command=self.activate_Right_stick_mouse)
        self.simpleConButton = ttk.Button(self.control_lf)
        self.simpleConButton.config(text='Controller')
        self.simpleConButton.grid(column='0', padx='10', pady='5', row='1', sticky='ew')
        self.simpleConButton.rowconfigure('1', weight='1')
        self.simpleConButton.columnconfigure('0', weight='1')
        self.simpleConButton.configure(command=self.createControllerWindow)
        self.control_lf.config(height='200', text='Controller')
        # self.control_lf.grid(column='0', padx='5', row='2', sticky='nsew')
        self.control_lf.grid(column='0', padx='5', row='2', columnspan='2', sticky='nsew')
        # self.Poke_statistic_lf = ttk.Labelframe(self.frame_1)
        # self.OpenPokeButton = ttk.Button(self.Poke_statistic_lf)
        # self.OpenPokeButton.config(text='技統計')
        # self.OpenPokeButton.grid(padx='10', pady='10', sticky='nsew')
        # self.OpenPokeButton.rowconfigure('0', pad='0', uniform='1', weight='1')
        # self.OpenPokeButton.columnconfigure('0', pad='0', uniform='1', weight='1')
        # self.OpenPokeButton.configure(command=self.createGetFromHomeWindow)
        # self.Poke_statistic_lf.config(height='200', text='PokemonHome連携', width='200')
        # self.Poke_statistic_lf.grid(column='1', padx='5', row='2', sticky='nsew')
        self.lf = ttk.Labelframe(self.frame_1)
        self.Command_nb = ttk.Notebook(self.lf)
        self.py_cb = ttk.Combobox(self.Command_nb)
        self.py_name = tk.StringVar()
        self.py_cb.config(state='readonly', textvariable=self.py_name)
        self.py_cb.pack(side='top')
        self.Command_nb.add(self.py_cb, padding='5', text='Python Command')
        self.mcu_cb = ttk.Combobox(self.Command_nb)
        self.mcu_name = tk.StringVar()
        self.mcu_cb.config(state='readonly', textvariable=self.mcu_name)
        self.mcu_cb.pack(side='top')
        self.Command_nb.add(self.mcu_cb, padding='5', text='Mcu Command')
        self.Command_nb.grid(column='0', columnspan='2', padx='5', pady='5', row='0', sticky='ew')
        self.reloadCommandButton = ttk.Button(self.lf)
        self.reloadCommandButton.config(text='Reload')
        self.reloadCommandButton.grid(column='0', padx='5', pady='5', row='1', sticky='ew')
        self.reloadCommandButton.configure(command=self.reloadCommands)
        self.startButton = ttk.Button(self.lf)
        self.startButton.config(text='Start')
        self.startButton.grid(column='1', padx='5', pady='5', row='1', sticky='ew')
        self.startButton.configure(command=self.startPlay)
        self.lf.config(height='200', text='Command')
        self.lf.grid(column='2', padx='5', row='1', rowspan='2', sticky='nsew')
        self.log_scroll = ScrollbarHelper(self.frame_1, scrolltype='both')
        self.logArea = tk.Text(self.log_scroll.container)
        self.logArea.config(blockcursor='true', height='10', insertunfocussed='none', maxundo='0')
        self.logArea.config(relief='flat', state='disabled', undo='false', width='50')
        self.logArea.pack(expand='true', fill='both', side='top')
        self.log_scroll.add_child(self.logArea)
        self.log_scroll.config(borderwidth='1', padding='1', relief='sunken')
        # TODO - self.log_scroll: code for custom option 'usemousewheel' not implemented.
        self.log_scroll.grid(column='3', padx='5', pady='5', row='0', rowspan='3', sticky='nsew')
        self.frame_1.config(height='720', padding='5', relief='flat', width='1280')
        self.frame_1.pack(expand='true', fill='both', side='top')
        self.frame_1.columnconfigure('3', weight='1')
        '''
        ここまで
        '''

        # 仮置フレームを削除
        self.frame_1_2.destroy()

        # 標準出力をログにリダイレクト
        sys.stdout = StdoutRedirector(self.logArea)
        # load settings file
        self.loadSettings()
        # 各tk変数に設定値をセット(コピペ簡単のため)
        self.is_show_realtime.set(self.settings.is_show_realtime.get())
        self.is_show_serial.set(self.settings.is_show_serial.get())
        self.is_use_keyboard.set(self.settings.is_use_keyboard.get())
        self.fps.set(self.settings.fps.get())
        self.show_size.set(self.settings.show_size.get())
        self.com_port.set(self.settings.com_port.get())
        self.camera_id.set(self.settings.camera_id.get())
        # 各コンボボックスを現在の設定値に合わせて表示
        self.fps_cb.current(self.fps_cb['values'].index(self.fps.get()))
        self.show_size_cb.current(
            self.show_size_cb['values'].index(self.show_size.get())
        )

        if os.name == 'nt':
            try:
                self.locateCameraCmbbox()
                self.camera_entry.config(state='disable')
            except:
                # Locate an entry instead whenever dll is not imported successfully
                self.camera_name_fromDLL.set("An error occurred while displaying the camera names in NT environment.")
                self._logger.warning("An error occurred while displaying the camera names in NT environment.")
                self.Camera_Name.config(state='disable')
        else:
            self.camera_name_fromDLL.set("Not nt environment so that cannot show Camera name.")
            self.Camera_Name.config(state='disable')
        # open up a camera
        self.camera = Camera(self.fps.get())
        self.openCamera()
        # activate serial communication
        self.ser = Sender.Sender(self.is_show_serial)
        self.activateSerial()
        self.activateKeyboard()
        self.preview = CaptureArea(self.camera,
                                   self.fps.get(),
                                   self.is_show_realtime,
                                   self.ser,
                                   self.camera_lf,
                                   *list(map(int, self.show_size.get().split("x")))
                                   )
        self.preview.config(cursor='crosshair')
        self.preview.grid(column='0', columnspan='7', row='2', padx='5', pady='5', sticky=tk.NSEW)
        self.loadCommands()

        self.show_size_tmp = self.show_size_cb['values'].index(self.show_size_cb.get())
        self.root.bind('<Key-F5>', self.ReloadCommandWithF5)
        self._logger.debug("Bind F5 key to reload commands")
        self.root.bind('<Key-F6>', self.StartCommandWithF6)
        self._logger.debug("Bind F6 key to execute commands")
        self.root.bind('<Key-Escape>', self.StopCommandWithEsc)
        self._logger.debug("Bind Escape key to stop commands")

        # Main widget
        self.mainwindow = self.frame_1

        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.preview.startCapture()

        self.menu = PokeController_Menubar(self)
        self.root.config(menu=self.menu)

        # logging.debug(f'python version: {sys.version}')

    def openCamera(self):
        self.camera.openCamera(self.camera_id.get())

    def assignCamera(self, event):
        if os.name == 'nt':
            self.camera_name_fromDLL.set(self.camera_dic[self.camera_id.get()])

    def locateCameraCmbbox(self):
        import clr
        clr.AddReference(r"..\DirectShowLib\DirectShowLib-2005")
        from DirectShowLib import DsDevice, FilterCategory

        # Get names of detected camera devices
        captureDevices = DsDevice.GetDevicesOfCat(FilterCategory.VideoInputDevice)
        self.camera_dic = {cam_id: device.Name for cam_id, device in enumerate(captureDevices)}

        self.camera_dic[str(max(list(self.camera_dic.keys())) + 1)] = 'Disable'
        self.Camera_Name['values'] = [device for device in self.camera_dic.values()]
        self._logger.debug(f"Camera list: {[device for device in self.camera_dic.values()]}")
        dev_num = len(self.camera_dic)

        if self.camera_id.get() > dev_num - 1:
            print('Inappropriate camera ID! -> set to 0')
            self._logger.debug('Inappropriate camera ID! -> set to 0')
            self.camera_id.set(0)
            if dev_num == 0:
                print('No camera devices can be found.')
                self._logger.debug('No camera devices can be found.')
        #
        self.camera_entry.bind('<KeyRelease>', self.assignCamera)
        self.Camera_Name.current(self.camera_id.get())

    def saveCapture(self):
        self.camera.saveCapture()

    def set_cameraid(self, event=None):
        keys = [k for k, v in self.camera_dic.items() if v == self.Camera_Name.get()]
        if keys:
            ret = keys[0]
        else:
            ret = None
        self.camera_id.set(ret)

    def applyFps(self, event=None):
        print('changed FPS to: ' + self.fps.get() + ' [fps]')
        self.preview.setFps(self.fps.get())

    def applyWindowSize(self, event=None):
        width, height = map(int, self.show_size.get().split("x"))
        self.preview.setShowsize(height, width)
        if self.show_size_tmp != self.show_size_cb['values'].index(self.show_size_cb.get()):
            ret = tkmsg.askokcancel('確認', "この画面サイズに変更しますか？")
        else:
            return

        if ret:
            self.show_size_tmp = self.show_size_cb['values'].index(self.show_size_cb.get())
        else:
            self.show_size_cb.current(self.show_size_tmp)
            width_bef, height_bef = map(int, self.show_size.get().split("x"))
            self.preview.setShowsize(height_bef, width_bef)
            # self.show_size_tmp = self.show_size_cb['values'].index(self.show_size_cb.get())

    def activateSerial(self):
        if self.ser.isOpened():
            print('Port is already opened and being closed.')
            self.ser.closeSerial()
            self.keyPress = None
            self.activateSerial()
        else:
            if self.ser.openSerial(self.com_port.get()):
                print('COM Port ' + str(self.com_port.get()) + ' connected successfully')
                self._logger.debug('COM Port ' + str(self.com_port.get()) + ' connected successfully')
                self.keyPress = KeyPress(self.ser)

    def activateKeyboard(self):
        if self.is_use_keyboard.get():
            # enable Keyboard as controller
            if self.keyboard is None:
                self.keyboard = SwitchKeyboardController(self.keyPress)
                self.keyboard.listen()

            # bind focus
            if os.name == 'nt':
                self.root.bind("<FocusIn>", self.onFocusInController)
                self.root.bind("<FocusOut>", self.onFocusOutController)

        else:
            if os.name == 'nt':  # NOTE: Idk why but self.keyboard.stop() makes crash on Linux
                if self.keyboard is not None:
                    # stop listening to keyboard events
                    self.keyboard.stop()
                    self.keyboard = None

                self.root.bind("<FocusIn>", lambda _: None)
                self.root.bind("<FocusOut>", lambda _: None)

    def onFocusInController(self, event):
        # enable Keyboard as controller
        if event.widget == self.root and self.keyboard is None:
            self.keyboard = SwitchKeyboardController(self.keyPress)
            self.keyboard.listen()

    def onFocusOutController(self, event):
        # stop listening to keyboard events
        if event.widget == self.root and not self.keyboard is None:
            self.keyboard.stop()
            self.keyboard = None

    def createControllerWindow(self):
        if not self.controller is None:
            self.controller.focus_force()
            return

        window = ControllerGUI(self.root, self.ser)
        window.protocol("WM_DELETE_WINDOW", self.closingController)
        self.controller = window

    def activate_Left_stick_mouse(self):
        self.preview.ApplyLStickMouse()

    def activate_Right_stick_mouse(self):
        self.preview.ApplyRStickMouse()

    # def createGetFromHomeWindow(self):
    #     if self.poke_treeview is not None:
    #         self.poke_treeview.focus_force()
    #         return
    #
    #     window2 = GetFromHomeGUI(self.root, self.settings.season, self.settings.is_SingleBattle)
    #     window2.protocol("WM_DELETE_WINDOW", self.closingGetFromHome)
    #     self.poke_treeview = window2

    def loadCommands(self):
        self.py_loader = CommandLoader(util.ospath('Commands/PythonCommands'),
                                       PythonCommandBase.PythonCommand)  # コマンドの読み込み
        self.mcu_loader = CommandLoader(util.ospath('Commands/McuCommands'), McuCommandBase.McuCommand)
        self.py_classes = self.py_loader.load()
        self.mcu_classes = self.mcu_loader.load()
        self.setCommandItems()
        self.assignCommand()

    def setCommandItems(self):
        self.py_cb['values'] = [c.NAME for c in self.py_classes]
        self.py_cb.current(0)
        self.mcu_cb['values'] = [c.NAME for c in self.mcu_classes]
        self.mcu_cb.current(0)

    def assignCommand(self):
        # 選択されているコマンドを取得する
        self.mcu_cur_command = self.mcu_classes[self.mcu_cb.current()]()  # MCUコマンドについて

        # pythonコマンドは画像認識を使うかどうかで分岐している
        cmd_class = self.py_classes[self.py_cb.current()]
        if issubclass(cmd_class, PythonCommandBase.ImageProcPythonCommand):
            try:  # 画像認識の際に認識位置を表示する引数追加。互換性のため従来のはexceptに。
                self.py_cur_command = cmd_class(self.camera, self.preview)
            except TypeError:
                self.py_cur_command = cmd_class(self.camera)
            except:
                self.py_cur_command = cmd_class(self.camera)


        else:
            self.py_cur_command = cmd_class()

        if self.Command_nb.index(self.Command_nb.select()) == 0:
            self.cur_command = self.py_cur_command
        else:
            self.cur_command = self.mcu_cur_command

    def reloadCommands(self):
        # 表示しているタブを読み取って、どのコマンドを表示しているか取得、リロード後もそれが選択されるようにする
        oldval_mcu = self.mcu_cb.get()
        oldval_py = self.py_cb.get()

        self.py_classes = self.py_loader.reload()
        self.mcu_classes = self.mcu_loader.reload()

        # Restore the command selecting state if possible
        self.setCommandItems()
        if oldval_mcu in self.mcu_cb['values']:
            self.mcu_cb.set(oldval_mcu)
        if oldval_py in self.py_cb['values']:
            self.py_cb.set(oldval_py)
        self.assignCommand()
        print('Finished reloading command modules.')
        self._logger.info("Reloaded commands.")

    def startPlay(self, *event):
        if self.cur_command is None:
            print('No commands have been assigned yet.')
            self._logger.info('No commands have been assigned yet.')

        # set and init selected command
        self.assignCommand()

        print(self.startButton["text"] + ' ' + self.cur_command.NAME)
        self._logger.info(self.startButton["text"] + ' ' + self.cur_command.NAME)
        self.cur_command.start(self.ser, self.stopPlayPost)

        self.startButton["text"] = "Stop"
        self.startButton["command"] = self.stopPlay
        self.reloadCommandButton["state"] = "disabled"

    def stopPlay(self):
        print(self.startButton["text"] + ' ' + self.cur_command.NAME)
        self._logger.info(self.startButton["text"] + ' ' + self.cur_command.NAME)
        self.startButton["state"] = "disabled"
        self.cur_command.end(self.ser)

    def stopPlayPost(self):
        self.startButton["text"] = "Start"
        self.startButton["command"] = self.startPlay
        self.startButton["state"] = "normal"
        self.reloadCommandButton["state"] = "normal"

    def run(self):
        self._logger.debug("Start Poke-Controller")
        self.mainwindow.mainloop()

    def exit(self):
        ret = tkmsg.askyesno('確認', 'Poke Controllerを終了しますか？')
        if ret:
            if self.ser.isOpened():
                self.ser.closeSerial()
                print("Serial disconnected")
                # self._logger.info("Serial disconnected")

            # stop listening to keyboard events
            if not self.keyboard is None:
                self.keyboard.stop()
                self.keyboard = None

            # save settings
            self.settings.is_show_realtime.set(self.is_show_realtime.get())
            self.settings.is_show_serial.set(self.is_show_serial.get())
            self.settings.is_use_keyboard.set(self.is_use_keyboard.get())
            self.settings.fps.set(self.fps.get())
            self.settings.show_size.set(self.show_size.get())
            self.settings.com_port.set(self.com_port.get())
            self.settings.camera_id.set(self.camera_id.get())

            self.settings.save()

            self.camera.destroy()
            cv2.destroyAllWindows()
            self._logger.debug("Stop Poke Controller")
            self.root.destroy()

    def closingController(self):
        self.controller.destroy()
        self.controller = None

    # def closingGetFromHome(self):
    #     self.poke_treeview.destroy()
    #     self.poke_treeview = None

    def loadSettings(self):
        self.settings = Settings.GuiSettings()
        self.settings.load()

    def ReloadCommandWithF5(self, *event):
        self.reloadCommands()

    def StartCommandWithF6(self, *event):
        if self.startButton["text"] == "Stop":
            print("Command is now working!")
            self._logger.debug("Command is now working!")
        elif self.startButton["text"] == "Start":
            self.startPlay()

    def StopCommandWithEsc(self, *event):
        if self.startButton["text"] == "Stop":
            self.stopPlay()


class StdoutRedirector(object):
    """
    標準出力をtextウィジェットにリダイレクトするクラス
    重いので止めました →# update_idletasks()で出力のたびに随時更新(従来はfor loopのときなどにまとめて出力されることがあった)
    """

    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.configure(state='normal')
        self.text_space.insert('end', string)
        self.text_space.see('end')
        # self.text_space.update_idletasks()
        self.text_space.configure(state='disabled')

    def flush(self):
        pass


if __name__ == '__main__':
    import tkinter as tk

    logger = PokeConLogger.root_logger()
    # logger.info('The root logger is created.')

    root = tk.Tk()
    app = PokeControllerApp(root)
    app.run()
