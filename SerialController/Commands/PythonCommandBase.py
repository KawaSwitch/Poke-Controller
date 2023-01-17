#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import cv2
import threading
from abc import abstractclassmethod
from time import sleep
import random
import time
from logging import getLogger, DEBUG, NullHandler
from os import path
import tkinter as tk
import tkinter.ttk as ttk

import Settings
from LineNotify import Line_Notify
from . import CommandBase
from .Keys import Button, Direction, KeyPress

import numpy as np


# the class For notifying stop signal is sent from Main window
class StopThread(Exception):
    pass


# Python command
class PythonCommand(CommandBase.Command):
    def __init__(self):
        super(PythonCommand, self).__init__()
        self.keys = None
        self.thread = None
        self.alive = True
        self.postProcess = None
        self.Line = Line_Notify()
        self.message_dialogue = None

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

    @abstractclassmethod
    def do(self):
        pass

    def do_safe(self, ser):
        if self.keys is None:
            self.keys = KeyPress(ser)

        try:
            if self.alive:
                self.do()
                self.finish()
        except StopThread:
            print('-- finished successfully. --')
            self._logger.info("Command finished successfully")
        except:
            if self.keys is None:
                self.keys = KeyPress(ser)
            print('interrupt')
            self._logger.warning('Command stopped unexpectedly')
            import traceback
            traceback.print_exc()
            self.keys.end()
            self.alive = False

    def start(self, ser, postProcess=None):
        self.alive = True
        self.postProcess = postProcess
        if not self.thread:
            self.thread = threading.Thread(target=self.do_safe, args=(ser,))
            self.thread.start()

    def end(self, ser):
        self.sendStopRequest()

    def sendStopRequest(self):
        if self.checkIfAlive():  # try if we can stop now
            self.alive = False
            print('-- sent a stop request. --')
            self._logger.info("Sending stop request")

    # NOTE: Use this function if you want to get out from a command loop by yourself
    def finish(self):
        self.alive = False
        self.end(self.keys.ser)

    # press button at duration times(s)
    def press(self, buttons, duration=0.1, wait=0.1):
        self.keys.input(buttons)
        self.wait(duration)
        self.keys.inputEnd(buttons)
        self.wait(wait)
        self.checkIfAlive()

    # press button at duration times(s) repeatedly
    def pressRep(self, buttons, repeat, duration=0.1, interval=0.1, wait=0.1):
        for i in range(0, repeat):
            self.press(buttons, duration, 0 if i == repeat - 1 else interval)
        self.wait(wait)

    # add hold buttons
    def hold(self, buttons, wait=0.1):
        self.keys.hold(buttons)
        self.wait(wait)

    # release holding buttons
    def holdEnd(self, buttons):
        self.keys.holdEnd(buttons)
        self.checkIfAlive()

    # do nothing at wait time(s)
    def short_wait(self, wait):
        current_time = time.perf_counter()
        while time.perf_counter() < current_time + wait:
            pass
        self.checkIfAlive()

    # do nothing at wait time(s)
    def wait(self, wait):
        if float(wait) > 0.1:
            sleep(wait)
        else:
            current_time = time.perf_counter()
            while time.perf_counter() < current_time + wait:
                pass
        self.checkIfAlive()
    
    def checkIfAlive(self):
        if not self.alive:
            self.keys.end()
            self.keys = None
            self.thread = None

            if not self.postProcess is None:
                self.postProcess()
                self.postProcess = None

            # raise exception for exit working thread
            self._logger.info('Exit from command successfully')
            raise StopThread('exit successfully')
        else:
            return True

    def dialogue(self, title: str, message: int | str | list, need=list):
        self.message_dialogue = tk.Toplevel()
        ret = PokeConDialogue(self.message_dialogue, title, message).ret_value(need)
        self.message_dialogue = None
        return ret

    def dialogue6widget(self, title: str, dialogue_list: list, need=list):
        self.message_dialogue = tk.Toplevel()
        ret = PokeConDialogue(self.message_dialogue, title, dialogue_list, mode=1).ret_value(need)
        self.message_dialogue = None
        return ret

    # Use time glitch

    # Controls the system time and get every-other-day bonus without any punishments
    def timeLeap(self, is_go_back=True):
        self.press(Button.HOME, wait=1)
        self.press(Direction.DOWN)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Button.A, wait=1.5)  # System Settings
        self.press(Direction.DOWN, duration=2, wait=0.5)

        self.press(Button.A, wait=0.3)  # System Settings > System
        self.press(Direction.DOWN)
        self.press(Direction.DOWN)
        self.press(Direction.DOWN)
        self.press(Direction.DOWN, wait=0.3)
        self.press(Button.A, wait=0.2)  # Date and Time
        self.press(Direction.DOWN, duration=0.7, wait=0.2)

        # increment and decrement
        if is_go_back:
            self.press(Button.A, wait=0.2)
            self.press(Direction.UP, wait=0.2)  # Increment a year
            self.press(Direction.RIGHT, duration=1.5)
            self.press(Button.A, wait=0.5)

            self.press(Button.A, wait=0.2)
            self.press(Direction.LEFT, duration=1.5)
            self.press(Direction.DOWN, wait=0.2)  # Decrement a year
            self.press(Direction.RIGHT, duration=1.5)
            self.press(Button.A, wait=0.5)

        # use only increment
        # for use of faster time leap
        else:
            self.press(Button.A, wait=0.2)
            self.press(Direction.RIGHT)
            self.press(Direction.RIGHT)
            self.press(Direction.UP, wait=0.2)  # increment a day
            self.press(Direction.RIGHT, duration=1)
            self.press(Button.A, wait=0.5)

        self.press(Button.HOME, wait=1)
        self.press(Button.HOME, wait=1)

    def LINE_text(self, txt="", token='token'):
        self.Line.send_text(txt, token)

    # direct serial
    def direct_serial(self, serialcommands: list, waittime: list):
        # 余計なものが付いている可能性があるので確認して削除する
        checkedcommands = []
        for row in serialcommands:
            checkedcommands.append(row.replace("\r", "").replace("\n", ""))
        self.keys.serialcommand_direct_send(checkedcommands, waittime)

    # Reload COM port (temporary function)
    def reload_com_port(self):
        if self.keys.ser.isOpened():
            print('Port is already opened and being closed.')
            self.keys.ser.closeSerial()
            # self.keyPress = None (ここでNoneはNGなはず)
            self.reload_com_port()
        else:
            if self.keys.ser.openSerial(Settings.GuiSettings().com_port.get(), Settings.GuiSettings().com_port_name.get(), Settings.GuiSettings().baud_rate.get()):
                print('COM Port ' + str(Settings.GuiSettings().com_port.get()) + ' connected successfully')
                self._logger.debug('COM Port ' + str(Settings.GuiSettings().com_port.get()) + ' connected successfully')
                # self.keyPress = None (ここでNoneはNGなはず)

class PokeConDialogue(object):
    def __init__(self, parent, title: str, message: int | str | list, mode=0):
        """
        pokecon用ダイアログ生成関数(注意:mode=0と1でmessageの取り扱いが大きく異なる。)
        mode | int: 0のときEntryのみ、1のとき6種類のwidgetに対応
        title | str: タイトル
        message | mode=0の場合 : int/str/list: Entryのラベル、mode=1の場合 : list[widget, widget, ...]: widgetごとの設定をリスト化したもの
        widget | list : widgetごとの設定(ウィジェットの種類によってリストの中身は異なる。以下を参照。)
        checkbox/entryの場合 : [type, subtitle, init] (例) ["check", "Check(例)", True]、["ENTRY", "Entry(例)", "初期値"]
        combobox/radiobutton/spinboxの場合 : [type, subtitle, selectlist, init] (例) ["Combo", "Combo(例)", ["hello", "world"], "hello"]、["RADIO", "Radio(例)", ["dog", "cat"],"dog"]、["Spin", "Spin(例)", list(map(str, range(10))), "3"]
        scaleの場合 : [type, subtitle, min, max, init, digit] (例) ["Scale", "scale(例)", 0, 100, 50.1, 2]
        type | str: widgetの種類(check/combo/entry/radio/spin/scaleのいずれか。大文字小文字は問わない)
        subtitle | str : widgetのタイトル
        init | checkboxの場合bool,scaleの場合int/float,その他str : 初期値
        selectlist | list : 項目のリスト
        min/max | int/float : scaleの最小値と最大値
        digit | int : 有効桁数
        return : なし
        """
        self._ls = None
        self.isOK = None

        self.message_dialogue = parent
        self.message_dialogue.title(title)
        self.message_dialogue.attributes("-topmost", True)
        self.message_dialogue.protocol("WM_DELETE_WINDOW", self.close_window)

        self.main_frame = tk.Frame(self.message_dialogue)
        self.inputs = ttk.Frame(self.main_frame)

        self.title_label = ttk.Label(self.main_frame, text=title, anchor='center')
        self.title_label.grid(column=0, columnspan=2, ipadx='10', ipady='10', row=0, sticky='nsew')

        self.dialogue_ls = {}
        x = self.message_dialogue.master.winfo_x()
        w = self.message_dialogue.master.winfo_width()
        y = self.message_dialogue.master.winfo_y()
        h = self.message_dialogue.master.winfo_height()
        w_ = self.message_dialogue.winfo_width()
        h_ = self.message_dialogue.winfo_height()
        self.message_dialogue.geometry(f"+{int(x+w/2-w_/2)}+{int(y+h/2-h_/2)}")

        if mode == 0:
            self.mode0(message)
        else:
            self.mode1(message)

        self.inputs.grid(column=0, columnspan=2, ipadx='10', ipady='10', row=1, sticky='nsew')
        self.inputs.grid_anchor('center')
        self.result = ttk.Frame(self.main_frame)
        self.OK = ttk.Button(self.result, command=self.ok_command)
        self.OK.configure(text='OK')
        self.OK.grid(column=0, row=1)
        self.Cancel = ttk.Button(self.result, command=self.cancel_command)
        self.Cancel.configure(text='Cancel')
        self.Cancel.grid(column=1, row=1, sticky='ew')
        self.result.grid(column=0, columnspan=2, pady=5, row=2, sticky='ew')
        self.result.grid_anchor('center')
        self.main_frame.pack()
        self.message_dialogue.master.wait_window(self.message_dialogue)

    def mode0(self, message):
        if type(message) is not list:
            message = [message]
        n = len(message)

        for i in range(n):
            self.dialogue_ls[message[i]] = tk.StringVar()
            label = ttk.Label(self.inputs, text=message[i])
            entry = ttk.Entry(self.inputs, textvariable=self.dialogue_ls[message[i]])
            label.grid(column=0, row=i, sticky='nsew', padx=3, pady=3)
            entry.grid(column=1, row=i, sticky='nsew', padx=3, pady=3)

    def mode1(self, dialogue_list):
        n = len(dialogue_list)
        frame = []

        scale_label_list = []   # scaleの値を表示するlabelを格納するリスト
        scale_index_list = []   # scaleが何番目のwidgetなのかを格納するリスト
        scale_digit_list = []   # scaleの有効桁数を格納するリスト

        def change_scale_value(event=None):   # scaleのバーを動かしたときにlabelの値を変更するための関数
            for i, (index, fmt) in enumerate(zip(scale_index_list, scale_digit_list)):
                if fmt != 0:
                    val = round(self.dialogue_ls[dialogue_list[index][1]].get(), fmt)
                    scale_label_list[i]["text"] = "%s" % val
                    self.dialogue_ls[dialogue_list[index][1]].set(val)
                else:
                    scale_label_list[i]["text"] = "%s" % self.dialogue_ls[dialogue_list[index][1]].get()

        for i in range(n):
            # widgetはすべてframeの中に入れる。scaleの場合、値を示すlabelもフレームの中に入れる。
            frame.append(ttk.LabelFrame(self.inputs, text=dialogue_list[i][1]))

            # Checkbox
            if dialogue_list[i][0].casefold() == "check".casefold():
                self.dialogue_ls[dialogue_list[i][1]] = tk.BooleanVar(value=dialogue_list[i][2])
                widget = ttk.Checkbutton(frame[i], variable=self.dialogue_ls[dialogue_list[i][1]])
                widget.grid(column=0, row=0, sticky='nsew', padx=3, pady=3)
            # Combobox
            elif dialogue_list[i][0].casefold() == "combo".casefold():
                self.dialogue_ls[dialogue_list[i][1]] = tk.StringVar(value=dialogue_list[i][3])
                widget = ttk.Combobox(frame[i], values=dialogue_list[i][2], textvariable=self.dialogue_ls[dialogue_list[i][1]])
                widget.grid(column=0, row=0, sticky='nsew', padx=3, pady=3)
                # widget.current(0)
            # Entry
            elif dialogue_list[i][0].casefold() == "entry".casefold():
                self.dialogue_ls[dialogue_list[i][1]] = tk.StringVar(value=dialogue_list[i][2])
                widget = ttk.Entry(frame[i], textvariable=self.dialogue_ls[dialogue_list[i][1]])
                widget.grid(column=0, row=0, sticky='nsew', padx=3, pady=3)
            # Radiobutton
            elif dialogue_list[i][0].casefold() == "radio".casefold():
                self.dialogue_ls[dialogue_list[i][1]] = tk.StringVar(value=dialogue_list[i][3])
                for j, text0 in enumerate(dialogue_list[i][2]):
                    widget = ttk.Radiobutton(frame[i], text=text0, variable=self.dialogue_ls[dialogue_list[i][1]], value=text0)
                    widget.grid(column=j, row=0, sticky='nsew', padx=3, pady=3)
            # Scale
            elif dialogue_list[i][0].casefold() == "scale".casefold():
                scale_index_list.append(i)
                scale_digit_list.append(dialogue_list[i][5])
                if dialogue_list[i][5] != 0:    # 浮動小数点数
                    self.dialogue_ls[dialogue_list[i][1]] = tk.DoubleVar(value=dialogue_list[i][4])
                    scale_label_list.append(tk.Label(frame[i], width=10, text="%s" % round(self.dialogue_ls[dialogue_list[i][1]].get(), dialogue_list[i][5])))
                else:   # 整数
                    self.dialogue_ls[dialogue_list[i][1]] = tk.IntVar(value=dialogue_list[i][4])
                    scale_label_list.append(tk.Label(frame[i], width=10, text="%s" % self.dialogue_ls[dialogue_list[i][1]].get()))
                widget = ttk.Scale(frame[i], from_=dialogue_list[i][2], to=dialogue_list[i][3], variable=self.dialogue_ls[dialogue_list[i][1]], command=change_scale_value)
                scale_label_list[-1].grid(column=0, row=0, sticky='nsew', padx=3, pady=3)
                widget.grid(column=1, row=0, sticky='nsew', padx=3, pady=3)
            # Spinbox
            elif dialogue_list[i][0].casefold() == "spin".casefold():
                self.dialogue_ls[dialogue_list[i][1]] = tk.StringVar(value=dialogue_list[i][3])
                widget = ttk.Spinbox(frame[i], values = dialogue_list[i][2], textvariable=self.dialogue_ls[dialogue_list[i][1]])
                widget.grid(column=0, row=0, sticky='nsew', padx=3, pady=3)

            frame[i].grid(column=0, row=i, sticky='nsew', padx=3, pady=3)

        # widgetのサイズをフレームのサイズに合わせる
        for i in range(n):
            if dialogue_list[i][0].casefold() == "scale".casefold():
                frame[i].grid_columnconfigure(0, weight=1)
                frame[i].grid_columnconfigure(1, weight=3)
            else:
                frame[i].grid_columnconfigure(0, weight=1)

    def ret_value(self, need):
        if self.isOK:
            if need == dict:
                return {k: v.get() for k, v in self.dialogue_ls.items()}
            elif need == list:
                return self._ls
            else:
                print(f"Wrong arg. Try Return list.")
                return self._ls
        else:
            return False

    def close_window(self):
        self.message_dialogue.destroy()
        self.isOK = False

    def ok_command(self):
        self._ls = [v.get() for k, v in self.dialogue_ls.items()]
        self.message_dialogue.destroy()
        self.isOK = True

    def cancel_command(self):
        self.message_dialogue.destroy()
        self.isOK = False


TEMPLATE_PATH = "./Template/"
def _get_template_filespec(template_path: str) -> str:
    """
    テンプレート画像ファイルのパスを取得する。
    入力が絶対パスの場合は、`TEMPLATE_PATH`につなげずに返す。
    Args:
        template_path (str): 画像パス
    Returns:
        str: _description_
    """
    if path.isabs(template_path):
        return template_path
    else:
        return path.join(TEMPLATE_PATH, template_path)


class ImageProcPythonCommand(PythonCommand):
    def __init__(self, cam, gui=None):
        super(ImageProcPythonCommand, self).__init__()

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.camera = cam
        self.Line = Line_Notify(self.camera)

        self.gui = gui

        self.gsrc = cv2.cuda_GpuMat()
        self.gtmpl = cv2.cuda_GpuMat()
        self.gresult = cv2.cuda_GpuMat()

    # Judge if current screenshot contains an image using template matching
    # It's recommended that you use gray_scale option unless the template color wouldn't be cared for performace
    # 現在のスクリーンショットと指定した画像のテンプレートマッチングを行います
    # 色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します
    def isContainTemplate(self, template_path, threshold=0.7, use_gray=True,
                          show_value=False, show_position=True, show_only_true_rect=True, ms=2000, crop=[], mask_path=None):
        src = self.camera.readFrame()
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if use_gray else src
        
        if len(crop) == 4:
            src = src[crop[1]: crop[3], crop[0]: crop[2]]

        template = cv2.imread(_get_template_filespec(template_path), cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)

        # mask用画像読み込み
        if mask_path == None:
            mask = None
            method = cv2.TM_CCOEFF_NORMED
        else:
            mask = cv2.imread(_get_template_filespec(mask_path), 0)
            method = cv2.TM_CCORR_NORMED

        w, h = template.shape[1], template.shape[0]

        res = cv2.matchTemplate(src, template, method, mask)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if show_value:
            print(template_path + ' ZNCC value: ' + str(max_val))

        top_left = max_loc
        bottom_right = (top_left[0] + w + 1, top_left[1] + h + 1)
        tag = str(time.perf_counter()) + str(random.random())
        if max_val >= threshold:
            if self.gui is not None and show_position:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='blue',
                                 tag=tag,
                                 ms=ms)
            return True
        else:
            if self.gui is not None and show_position and not show_only_true_rect:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='red',
                                 tag=tag,
                                 ms=ms)
            return False
    
    # 現在のスクリーンショットと指定した複数の画像のテンプレートマッチングを行います
    # 相関値が最も大きい値となった画像のインデックス、各画像のテンプレートマッチングの閾値、閾値判定結果を返します。
    # 色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します
    def isContainTemplate_max(self, template_path_list, threshold=0.7, use_gray=True,
                              show_value=False, show_position=True, show_only_true_rect=True, ms=2000, crop=[]):
        src = self.camera.readFrame()
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if use_gray else src
        
        if len(crop) == 4:
            src = src[crop[1]: crop[3], crop[0]: crop[2]]
        
        max_val_list = []
        judge_threshold_list = []
        for template_path in template_path_list:
            template = cv2.imread(_get_template_filespec(template_path), cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)
            w, h = template.shape[1], template.shape[0]

            method = cv2.TM_CCOEFF_NORMED
            res = cv2.matchTemplate(src, template, method)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            if show_value:
                print(template_path + ' ZNCC value: ' + str(max_val))

            top_left = max_loc
            bottom_right = (top_left[0] + w + 1, top_left[1] + h + 1)
            tag = str(time.perf_counter()) + str(random.random())
            max_val_list.append(max_val)
            judge_threshold_list.append(max_val >= threshold)

            if max_val >= threshold:
                if self.gui is not None and show_position:
                    # self.gui.delete("ImageRecRect")
                    self.gui.ImgRect(*top_left,
                                    *bottom_right,
                                    outline='blue',
                                    tag=tag,
                                    ms=ms)
            else:
                if self.gui is not None and show_position and not show_only_true_rect:
                    # self.gui.delete("ImageRecRect")
                    self.gui.ImgRect(*top_left,
                                    *bottom_right,
                                    outline='red',
                                    tag=tag,
                                    ms=ms)

        return np.argmax(max_val_list), max_val_list, judge_threshold_list

    try:
        def isContainTemplateGPU(self, template_path, threshold=0.7, use_gray=True,
                                 show_value=False, not_show_false=True):
            src = self.camera.readFrame()
            src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if use_gray else src

            self.gsrc.upload(src)

            template = cv2.imread(_get_template_filespec(template_path), cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)
            self.gtmpl.upload(template)

            method = cv2.TM_CCOEFF_NORMED
            matcher = cv2.cuda.createTemplateMatching(cv2.CV_8UC1, method)
            gresult = matcher.match(self.gsrc, self.gtmpl)
            resultg = gresult.download()
            _, max_val, _, max_loc = cv2.minMaxLoc(resultg)

            if show_value:
                print(template_path + ' ZNCC value: ' + str(max_val))

            if max_val >= threshold:
                # if use_gray:
                #     src = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
                #
                # top_left = max_loc
                # bottom_right = (top_left[0] + w, top_left[1] + h)
                # cv2.rectangle(src, top_left, bottom_right, (255, 0, 255), 2)
                return True
            else:
                return False
    except ModuleNotFoundError:
        pass

    # Get interframe difference binarized image
    # フレーム間差分により2値化された画像を取得
    def getInterframeDiff(self, frame1, frame2, frame3, threshold):
        diff1 = cv2.absdiff(frame1, frame2)
        diff2 = cv2.absdiff(frame2, frame3)

        diff = cv2.bitwise_and(diff1, diff2)

        # binarize
        img_th = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

        # remove noise
        mask = cv2.medianBlur(img_th, 3)
        return mask

    def LINE_image(self, txt="", token='token'):
        try:
            self.Line.send_text_n_image(txt, token)
        except:
            pass

