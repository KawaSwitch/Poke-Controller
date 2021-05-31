import configparser
import os
import tkinter as tk
import tkinter.ttk as ttk
from logging import getLogger, DEBUG, NullHandler

from pynput.keyboard import Listener


class PokeKeycon:
    SETTING_PATH = os.path.join(os.path.dirname(__file__), "settings.ini")

    def __init__(self, master=None, **kw):
        self.master = master
        self.kc = tk.Toplevel(master)
        self.kc.title('Key Config')
        self.listener = None
        self.setting = configparser.ConfigParser()
        self.setting.optionxform = str

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.kc.resizable(False, False)

        # Initialize style
        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame', background='white')
        s.configure('Frame1.TFrame', background='#00c3e3')
        s.configure('Frame2.TFrame', background='#ff4554')

        # ttk.Frame.__init__(self, master, **kw)
        # build ui
        self.key_config_frame = ttk.Frame(self.kc)
        self.frame_2 = ttk.Frame(self.key_config_frame, style='Frame1.TFrame')

        self.label_ZL = ttk.Label(self.frame_2)
        self.label_ZL.configure(padding='5', text='ZL', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_ZL.grid(sticky='e')
        self.entry_ZL = ttk.Entry(self.frame_2)
        self.ZL = tk.StringVar()
        self.entry_ZL.configure(state='readonly', textvariable=self.ZL)
        self.entry_ZL.grid(column='1', padx='5', pady='5', row='0')

        self.label_L = ttk.Label(self.frame_2)
        self.label_L.configure(padding='5', text='L', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_L.grid(row='1', sticky='e')
        self.entry_L = ttk.Entry(self.frame_2)
        self.L = tk.StringVar()
        self.entry_L.configure(state='readonly', textvariable=self.L)
        self.entry_L.grid(column='1', padx='5', pady='5', row='1')

        self.label_MINUS = ttk.Label(self.frame_2)
        self.label_MINUS.configure(padding='5', text='MINUS', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_MINUS.grid(row='2', sticky='e')
        self.entry_MINUS = ttk.Entry(self.frame_2)
        self.MINUS = tk.StringVar()
        self.entry_MINUS.configure(state='readonly', textvariable=self.MINUS)
        self.entry_MINUS.grid(column='1', padx='5', pady='5', row='2')

        self.label_HAT_UP = ttk.Label(self.frame_2)
        self.label_HAT_UP.configure(padding='5', text='HAT UP', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_HAT_UP.grid(row='3', sticky='e')
        self.entry_HAT_UP = ttk.Entry(self.frame_2)
        self.HAT_UP = tk.StringVar()
        self.entry_HAT_UP.configure(state='readonly', textvariable=self.HAT_UP)
        self.entry_HAT_UP.grid(column='1', padx='5', pady='5', row='3')

        self.label__HAT_LEFT = ttk.Label(self.frame_2)
        self.label__HAT_LEFT.configure(padding='5', text='HAT LEFT', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label__HAT_LEFT.grid(row='4', sticky='e')
        self.entry_HAT_LEFT = ttk.Entry(self.frame_2)
        self.HAT_LEFT = tk.StringVar()
        self.entry_HAT_LEFT.configure(state='readonly', textvariable=self.HAT_LEFT)
        self.entry_HAT_LEFT.grid(column='1', padx='5', pady='5', row='4')

        self.label_HAT_RIGHT = ttk.Label(self.frame_2)
        self.label_HAT_RIGHT.configure(padding='5', text='HAT RIGHT', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_HAT_RIGHT.grid(row='5', sticky='e')
        self.entry_HAT_RIGHT = ttk.Entry(self.frame_2)
        self.HAT_RIGHT = tk.StringVar()
        self.entry_HAT_RIGHT.configure(state='readonly', textvariable=self.HAT_RIGHT)
        self.entry_HAT_RIGHT.grid(column='1', padx='5', pady='5', row='5')

        self.label_HAT_DOWN = ttk.Label(self.frame_2)
        self.label_HAT_DOWN.configure(padding='5', text='HAT DOWN', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_HAT_DOWN.grid(row='6', sticky='e')
        self.entry_HAT_DOWN = ttk.Entry(self.frame_2)
        self.HAT_DOWN = tk.StringVar()
        self.entry_HAT_DOWN.configure(state='readonly', textvariable=self.HAT_DOWN)
        self.entry_HAT_DOWN.grid(column='1', padx='5', pady='5', row='6')

        self.label_CAPTURE = ttk.Label(self.frame_2)
        self.label_CAPTURE.configure(padding='5', text='CAPTURE', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_CAPTURE.grid(row='7', sticky='e')
        self.entry_CAPTURE = ttk.Entry(self.frame_2)
        self.CAPTURE = tk.StringVar()
        self.entry_CAPTURE.configure(state='readonly', textvariable=self.CAPTURE)
        self.entry_CAPTURE.grid(column='1', padx='5', pady='5', row='7')

        self.label_LCLICK = ttk.Label(self.frame_2)
        self.label_LCLICK.configure(padding='5', text='L CLICK', background='#00c3e3', font='{游ゴシック} 12 {bold}')
        self.label_LCLICK.grid(row='8', sticky='e')
        self.entry_LCLICK = ttk.Entry(self.frame_2)
        self.LCLICK = tk.StringVar()
        self.entry_LCLICK.configure(state='readonly', textvariable=self.LCLICK)
        self.entry_LCLICK.grid(column='1', padx='5', pady='5', row='8')

        self.frame_2.configure(height='200', padding='10', relief='groove', width='200')
        self.frame_2.grid(column='0', row='1', sticky='nsew')
        self.frame_2.rowconfigure('1', pad='5')
        self.frame_2.columnconfigure('0', pad='5')

        self.frame_2_3 = ttk.Frame(self.key_config_frame, style='Frame2.TFrame')

        self.label_ZR = ttk.Label(self.frame_2_3)
        self.label_ZR.configure(padding='5', text='ZR', background='#ff4554', foreground='#ffffff',
                                font='{游ゴシック} 12 {bold}')
        self.label_ZR.grid(row='0', sticky='e')
        self.entry_ZR = ttk.Entry(self.frame_2_3)
        self.ZR = tk.StringVar()
        self.entry_ZR.configure(state='readonly', textvariable=self.ZR)
        self.entry_ZR.grid(column='1', padx='5', pady='5', row='0')

        self.label_R = ttk.Label(self.frame_2_3)
        self.label_R.configure(padding='5', text='R', background='#ff4554', foreground='#ffffff',
                               font='{游ゴシック} 12 {bold}')
        self.label_R.grid(row='1', sticky='e')
        self.entry_R = ttk.Entry(self.frame_2_3)
        self.R = tk.StringVar()
        self.entry_R.configure(state='readonly', textvariable=self.R)
        self.entry_R.grid(column='1', padx='5', pady='5', row='1')

        self.label_PLUS = ttk.Label(self.frame_2_3)
        self.label_PLUS.configure(padding='5', text='PLUS', background='#ff4554', foreground='#ffffff',
                                  font='{游ゴシック} 12 {bold}')
        self.label_PLUS.grid(row='2', sticky='e')
        self.entry_PLUS = ttk.Entry(self.frame_2_3)
        self.PLUS = tk.StringVar()
        self.entry_PLUS.configure(state='readonly', textvariable=self.PLUS)
        self.entry_PLUS.grid(column='1', padx='5', pady='5', row='2')

        self.label_A = ttk.Label(self.frame_2_3)
        self.label_A.configure(padding='5', text='A', background='#ff4554', foreground='#ffffff',
                               font='{游ゴシック} 12 {bold}')
        self.label_A.grid(row='3', sticky='e')
        self.entry_A = ttk.Entry(self.frame_2_3)
        self.A = tk.StringVar()
        self.entry_A.configure(state='readonly', textvariable=self.A)
        self.entry_A.grid(column='1', padx='5', pady='5', row='3')

        self.label__B = ttk.Label(self.frame_2_3)
        self.label__B.configure(padding='5', text='B', background='#ff4554', foreground='#ffffff',
                                font='{游ゴシック} 12 {bold}')
        self.label__B.grid(row='4', sticky='e')
        self.entry_B = ttk.Entry(self.frame_2_3)
        self.B = tk.StringVar()
        self.entry_B.configure(state='readonly', textvariable=self.B)
        self.entry_B.grid(column='1', padx='5', pady='5', row='4')

        self.label_X = ttk.Label(self.frame_2_3)
        self.label_X.configure(padding='5', text='X', background='#ff4554', foreground='#ffffff',
                               font='{游ゴシック} 12 {bold}')
        self.label_X.grid(row='5', sticky='e')
        self.entry_X = ttk.Entry(self.frame_2_3)
        self.X = tk.StringVar()
        self.entry_X.configure(state='readonly', textvariable=self.X)
        self.entry_X.grid(column='1', padx='5', pady='5', row='5')

        self.label_Y = ttk.Label(self.frame_2_3)
        self.label_Y.configure(padding='5', text='Y', background='#ff4554', foreground='#ffffff',
                               font='{游ゴシック} 12 {bold}')
        self.label_Y.grid(row='6', sticky='e')
        self.entry_Y = ttk.Entry(self.frame_2_3)
        self.Y = tk.StringVar()
        self.entry_Y.configure(state='readonly', textvariable=self.Y)
        self.entry_Y.grid(column='1', padx='5', pady='5', row='6')

        self.label_HOME = ttk.Label(self.frame_2_3)
        self.label_HOME.configure(padding='5', text='HOME', background='#ff4554', foreground='#ffffff',
                                  font='{游ゴシック} 12 {bold}')
        self.label_HOME.grid(row='7', sticky='e')
        self.entry_HOME = ttk.Entry(self.frame_2_3)
        self.HOME = tk.StringVar()
        self.entry_HOME.configure(state='readonly', textvariable=self.HOME)
        self.entry_HOME.grid(column='1', padx='5', pady='5', row='7')

        self.label_RCLICK = ttk.Label(self.frame_2_3)
        self.label_RCLICK.configure(padding='5', text='R CLICK', background='#ff4554', foreground='#ffffff',
                                    font='{游ゴシック} 12 {bold}')
        self.label_RCLICK.grid(row='8', sticky='e')
        self.entry_RCLICK = ttk.Entry(self.frame_2_3)
        self.RCLICK = tk.StringVar()
        self.entry_RCLICK.configure(state='readonly', textvariable=self.RCLICK)
        self.entry_RCLICK.grid(column='1', padx='5', pady='5', row='8')

        self.frame_2_3.configure(height='200', padding='10', relief='groove', width='200')
        self.frame_2_3.grid(column='1', row='1', sticky='nsew')
        self.frame_2_3.rowconfigure('1', pad='5')
        self.frame_2_3.columnconfigure('1', pad='5')

        self.frame_button = ttk.Frame(self.key_config_frame)
        self.apply_button = ttk.Button(self.frame_button)
        self.apply_button.configure(text='適用')
        self.apply_button.grid(column='0', padx='10', sticky='e')
        self.apply_button.configure(command=self.apply_setting)
        self.frame_button.configure(height='200', width='200')
        self.frame_button.grid(column='1', columnspan='1', row='2', sticky='e')

        self.key_config_frame.configure(height='200', width='200')
        self.key_config_frame.pack(side='top')

        # Main widget
        self.mainwindow = self.key_config_frame

        self.load_config()

        self.entry_ZL.bind('<FocusIn>', lambda x: self.onFocusInController(self.ZL, 'Button.ZL'))
        self.entry_ZL.bind('<FocusOut>', self.onFocusOutController)
        self.entry_L.bind('<FocusIn>', lambda x: self.onFocusInController(self.L, 'Button.L'))
        self.entry_L.bind('<FocusOut>', self.onFocusOutController)
        self.entry_LCLICK.bind('<FocusIn>', lambda x: self.onFocusInController(self.LCLICK, 'Button.LCLICK'))
        self.entry_LCLICK.bind('<FocusOut>', self.onFocusOutController)
        self.entry_ZR.bind('<FocusIn>', lambda x: self.onFocusInController(self.ZR, 'Button.ZR'))
        self.entry_ZR.bind('<FocusOut>', self.onFocusOutController)
        self.entry_R.bind('<FocusIn>', lambda x: self.onFocusInController(self.R, 'Button.R'))
        self.entry_R.bind('<FocusOut>', self.onFocusOutController)
        self.entry_RCLICK.bind('<FocusIn>', lambda x: self.onFocusInController(self.RCLICK, 'Button.RCLICK'))
        self.entry_RCLICK.bind('<FocusOut>', self.onFocusOutController)
        self.entry_MINUS.bind('<FocusIn>', lambda x: self.onFocusInController(self.MINUS, 'Button.MINUS'))
        self.entry_MINUS.bind('<FocusOut>', self.onFocusOutController)
        self.entry_CAPTURE.bind('<FocusIn>', lambda x: self.onFocusInController(self.CAPTURE, 'Button.CAPTURE'))
        self.entry_CAPTURE.bind('<FocusOut>', self.onFocusOutController)
        self.entry_A.bind('<FocusIn>', lambda x: self.onFocusInController(self.A, 'Button.A'))
        self.entry_A.bind('<FocusOut>', self.onFocusOutController)
        self.entry_B.bind('<FocusIn>', lambda x: self.onFocusInController(self.B, 'Button.B'))
        self.entry_B.bind('<FocusOut>', self.onFocusOutController)
        self.entry_X.bind('<FocusIn>', lambda x: self.onFocusInController(self.X, 'Button.X'))
        self.entry_X.bind('<FocusOut>', self.onFocusOutController)
        self.entry_Y.bind('<FocusIn>', lambda x: self.onFocusInController(self.Y, 'Button.Y'))
        self.entry_Y.bind('<FocusOut>', self.onFocusOutController)
        self.entry_PLUS.bind('<FocusIn>', lambda x: self.onFocusInController(self.PLUS, 'Button.PLUS'))
        self.entry_PLUS.bind('<FocusOut>', self.onFocusOutController)
        self.entry_HOME.bind('<FocusIn>', lambda x: self.onFocusInController(self.HOME, 'Button.HOME'))
        self.entry_HOME.bind('<FocusOut>', self.onFocusOutController)

        self.entry_HAT_UP.bind('<FocusIn>', lambda x: self.onFocusInController(self.HAT_UP, 'Hat.TOP'))
        self.entry_HAT_UP.bind('<FocusOut>', self.onFocusOutController)
        self.entry_HAT_RIGHT.bind('<FocusIn>', lambda x: self.onFocusInController(self.HAT_RIGHT, 'Hat.RIGHT'))
        self.entry_HAT_RIGHT.bind('<FocusOut>', self.onFocusOutController)
        self.entry_HAT_DOWN.bind('<FocusIn>', lambda x: self.onFocusInController(self.HAT_DOWN, 'Hat.BTM'))
        self.entry_HAT_DOWN.bind('<FocusOut>', self.onFocusOutController)
        self.entry_HAT_LEFT.bind('<FocusIn>', lambda x: self.onFocusInController(self.HAT_LEFT, 'Hat.LEFT'))
        self.entry_HAT_LEFT.bind('<FocusOut>', self.onFocusOutController)

    def run(self):
        self.mainwindow.mainloop()

    def onFocusInController(self, var, button_name):
        # enable Keyboard as controller
        # print(event, var)
        self.listener = Listener(
            on_press=lambda ev: self.on_press(ev, var=var),
            on_release=lambda ev: self.on_release(ev, var=var, button_name=button_name))
        self.listener.start()
        self._logger.debug("Activate key config window")

    def onFocusOutController(self, event):
        self.listener.stop()
        self.listener = None

    def on_press(self, key, var):
        try:
            # print('alphanumeric key {0} pressed'.format(key.char))
            var.set(key.char)
        except AttributeError:
            var.set(key)
            # print(var)
            # print('special key {0} pressed'.format(key))

    def on_release(self, key, var, button_name):
        try:
            spc = button_name.split(".")[0]
            self._logger.debug(f"Released key :{var.get()}")
            self.setting[f'KeyMap-{spc}'][button_name] = var.get()
        except:
            pass
        # print(f'{key} released')

    def load_config(self):
        if os.path.isfile(self.SETTING_PATH):
            self.setting.read(self.SETTING_PATH, encoding='utf-8')

        self.ZL.set(self.setting['KeyMap-Button']['Button.ZL'])
        self.L.set(self.setting['KeyMap-Button']['Button.L'])
        self.LCLICK.set(self.setting['KeyMap-Button']['Button.LCLICK'])
        self.ZR.set(self.setting['KeyMap-Button']['Button.ZR'])
        self.R.set(self.setting['KeyMap-Button']['Button.R'])
        self.RCLICK.set(self.setting['KeyMap-Button']['Button.RCLICK'])
        self.MINUS.set(self.setting['KeyMap-Button']['Button.MINUS'])
        self.CAPTURE.set(self.setting['KeyMap-Button']['Button.CAPTURE'])
        self.A.set(self.setting['KeyMap-Button']['Button.A'])
        self.B.set(self.setting['KeyMap-Button']['Button.B'])
        self.X.set(self.setting['KeyMap-Button']['Button.X'])
        self.Y.set(self.setting['KeyMap-Button']['Button.Y'])
        self.PLUS.set(self.setting['KeyMap-Button']['Button.PLUS'])
        self.HOME.set(self.setting['KeyMap-Button']['Button.HOME'])
        self.HAT_UP.set(self.setting['KeyMap-Hat']['Hat.TOP'])
        self.HAT_DOWN.set(self.setting['KeyMap-Hat']['Hat.BTM'])
        self.HAT_LEFT.set(self.setting['KeyMap-Hat']['Hat.LEFT'])
        self.HAT_RIGHT.set(self.setting['KeyMap-Hat']['Hat.RIGHT'])

    def save_config(self):

        self.setting['KeyMap-Button']['Button.ZL'] = self.ZL.get()
        self.setting['KeyMap-Button']['Button.L'] = self.L.get()
        self.setting['KeyMap-Button']['Button.LCLICK'] = self.LCLICK.get()
        self.setting['KeyMap-Button']['Button.ZR'] = self.ZR.get()
        self.setting['KeyMap-Button']['Button.R'] = self.R.get()
        self.setting['KeyMap-Button']['Button.RCLICK'] = self.RCLICK.get()
        self.setting['KeyMap-Button']['Button.MINUS'] = self.MINUS.get()
        self.setting['KeyMap-Button']['Button.CAPTURE'] = self.CAPTURE.get()
        self.setting['KeyMap-Button']['Button.A'] = self.A.get()
        self.setting['KeyMap-Button']['Button.B'] = self.B.get()
        self.setting['KeyMap-Button']['Button.X'] = self.X.get()
        self.setting['KeyMap-Button']['Button.Y'] = self.Y.get()
        self.setting['KeyMap-Button']['Button.PLUS'] = self.PLUS.get()
        self.setting['KeyMap-Button']['Button.HOME'] = self.HOME.get()

        self.setting['KeyMap-Hat']['Hat.TOP'] = self.HAT_UP.get()
        self.setting['KeyMap-Hat']['Hat.RIGHT'] = self.HAT_RIGHT.get()
        self.setting['KeyMap-Hat']['Hat.BTM'] = self.HAT_DOWN.get()
        self.setting['KeyMap-Hat']['Hat.LEFT'] = self.HAT_LEFT.get()

        with open(self.SETTING_PATH, 'w', encoding='utf-8') as file:
            self.setting.write(file)

    def apply_setting(self):
        with open(self.SETTING_PATH, 'w', encoding='utf-8') as file:
            self._logger.debug("Apply key setting")
            self.setting.write(file)
        if self.listener is not None:
            self.listener.stop()

    def close(self):
        self.kc.withdraw()
        if self.listener is not None:
            self.listener.stop()

    def bind(self, event, func):
        self.kc.bind(event, func)

    def protocol(self, event, func):
        self.kc.protocol(event, func)

    def focus_force(self):
        self.kc.focus_force()
        self.kc.deiconify()

    def destroy(self):
        if self.listener is not None:
            self.listener.stop()
        self.kc.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = PokeKeycon(root)
    app.run()
