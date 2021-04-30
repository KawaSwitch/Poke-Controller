#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from Commands.Keys import Button, Direction, Hat
from Commands.PythonCommandBase import PythonCommand
# import numpy as np
from scipy.sparse.csgraph import shortest_path  # , floyd_warshall, dijkstra, bellman_ford, johnson
from scipy.sparse import csr_matrix

serial = {0: '-1',
          1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '0', 11: '@', 12: 'BS',
          13: 'Q', 14: 'W', 15: 'E', 16: 'R', 17: 'T', 18: 'Y', 19: 'U', 20: 'I', 21: 'O', 22: 'P', 23: '=',
          24: 'A', 25: 'S', 26: 'D', 27: 'F', 28: 'G', 29: 'H', 30: 'J', 31: 'K', 32: 'L', 33: '&', 34: ';',
          35: 'Z', 36: 'X', 37: 'C', 38: 'V', 39: 'B', 40: 'N', 41: 'M', 42: '*', 43: '#', 44: '!', 45: '?',
          46: 'SelectKeyboard', 47: 'Shift', 48: '#+=', 49: 'nl_1', 50: 'nl_2', 51: 'nl_3',
          52: 'ok_1', 53: 'ok_2', 54: 'ok_3', 55: 'blank_1', 56: 'blank_2', 57: 'blank_3', 58: 'blank_4',
          59: 'blank_5', 60: 'blank_6', 61: 'blank_7', 62: 'blank_8', }
serial_inv = {v: k for k, v in serial.items()}
serial_graph_list = [[],
                     # 1-5
                     [2, 13, 12], [1, 3, 14], [2, 4, 15], [3, 5, 16], [4, 6, 17],
                     # 6-10
                     [5, 7, 18], [6, 8, 19], [7, 9, 20], [8, 10, 21], [9, 11, 22],
                     # 11-15 @ ~ E
                     [10, 12, 23], [11, 49, 1], [1, 24, 14, 49], [2, 13, 15, 25], [3, 14, 16, 26],
                     # 16-20 R ~ I
                     [4, 15, 17, 27], [5, 16, 18, 28], [6, 17, 19, 29], [7, 18, 20, 30], [8, 19, 21, 31],
                     # 21-25 O ~ S
                     [9, 20, 22, 32], [10, 21, 23, 33], [11, 22, 34, 49], [13, 25, 35, 50], [14, 24, 26, 36],
                     # 26-30 D ~ J
                     [15, 25, 27, 37], [16, 26, 28, 38], [17, 27, 29, 39], [18, 28, 30, 40], [19, 29, 31, 41],
                     # 31-35 J ~ Z
                     [20, 30, 32, 42], [21, 31, 33, 43], [22, 32, 34, 44], [23, 33, 45, 50], [24, 46, 36, 53],
                     # 36-40 X ~ N
                     [25, 35, 37, 47], [26, 36, 38, 48], [27, 37, 39, 55], [28, 38, 40, 56], [29, 39, 41, 57],
                     # 41-45 M ~ ?
                     [30, 40, 42, 58], [31, 41, 43, 59], [32, 42, 44, 60], [33, 43, 45, 61], [34, 44, 62, 53],
                     # 46-50
                     [35, 47, 54], [36, 46, 48], [37, 47, 55], [12, 23, 13, 52], [12, 34, 24, 53],
                     # 51-56
                     [12, 34, 24, 54], [49, 45, 35], [45, 35, 50], [55, 46, 51], [38, 48, 54], [39, 48, 54],
                     # 57-62
                     [40, 48, 54], [41, 48, 54], [42, 48, 54], [43, 48, 54], [44, 48, 54], [45, 48, 54]]


class InputKeyboard(PythonCommand):
    NAME = 'シリアル入力'

    def __init__(self):
        super().__init__()
        self.s = 'F105LP98GMFCB3RA'  # 入力したい文字列
        self.now_dict = serial_graph_list
        self.now_dict_ = serial
        self.now_dict_inv = serial_inv
        self.graph = None
        self.d = None
        self.p = None
        self.n = None
        self.MakeGraph()
        self.pos = 1  # 初期位置

    def MakeGraph(self):
        self.n = len(self.now_dict)
        self.graph = [[0] * self.n for _ in range(self.n)]  # 隣接行列
        for i, g_i in enumerate(self.now_dict):
            for j in g_i:
                self.graph[i][j] = 1
        # for i in self.graph:
        # print(" ".join(list(map(str, i))))

        a = csr_matrix(self.graph)
        self.d, self.p = shortest_path(a, return_predecessors=True)

    def do(self):
        input_char = 0
        for i in self.s:
            print(self.now_dict_[self.now_dict_inv[i]])
            t = GetPath(self.pos, self.now_dict_inv[i], self.p)
            print(t)
            stick = False
            stick = self.Move(t, stick)
            if not stick:
                self.press(Button.A, wait=0.03, duration=0.05)
            input_char += 1

    def Move(self, t, stick):  # 移動のための関数
        for j in range(len(t) - 1):
            if t[j + 1] == 1 and t[j] == 12:
                self.press(Direction.RIGHT, wait=0.03, duration=0.05)
            if t[j + 1] == 12:
                if t[j] in [49, 50, 51]:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
                elif t[j] == 1:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 11:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
            elif t[j + 1] == 13:  # Q
                if t[j] == 49:
                    self.press(Direction.RIGHT, wait=0.1, duration=0.05)
                elif t[j] == 1:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
                elif t[j] == 14:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 24:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 23:  # =
                if t[j] == 22:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 11:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
                elif t[j] == 49:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 34:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 24:  # A
                if t[j] in [50, 51]:
                    self.press(Direction.RIGHT, wait=0.1, duration=0.05)
                elif t[j] == 13:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
                elif t[j] == 25:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 35:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 34:  # ;
                if t[j] == 33:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 23:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
                elif t[j] in [50, 51]:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 45:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 35:  # Z
                if t[j] in [52, 53]:
                    self.press(Direction.RIGHT, wait=0.1, duration=0.05)
                elif t[j] == 24:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
                elif t[j] == 36:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 46:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] in [38, 39, 40, 41, 42, 43, 44] and t[j + 1] - t[j] == -17:  # Z
                self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 45:  # ?
                if t[j] == 44:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 34:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
                elif t[j] in [52, 53]:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 62:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 48 and t[j] in [55, 56, 57, 58, 59, 60, 61, 62]:
                self.press(Direction.LEFT, wait=0.03, duration=0.05)

            elif t[j + 1] == 49:
                if t[j] == 12:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
                elif t[j] == 23:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 13:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 52:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 50:
                if t[j] == 34:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 24:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 53:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 51:
                if t[j] == 54:
                    self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] == 52:
                if t[j] == 49:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j + 1] == 53:
                if t[j] == 45:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 35:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 50:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j + 1] == 54:
                if t[j] in [55, 56, 57, 58, 59, 60, 61, 62]:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 46:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 51:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j + 1] == 55:
                if t[j] == 48:
                    self.press(Direction.RIGHT, wait=0.03, duration=0.05)
                elif t[j] == 54:
                    self.press(Direction.LEFT, wait=0.03, duration=0.05)
                elif t[j] == 38:
                    self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j + 1] in [56, 57, 58, 59, 60, 61, 62] and t[j + 1] - t[j] == 17:
                self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] == 1:
                self.press(Direction.RIGHT, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] == -1:
                self.press(Direction.LEFT, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] in [11, 12]:
                self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] in [-11, -12]:
                self.press(Direction.UP, wait=0.03, duration=0.05)
            if t[j + 1] not in list(range(67, self.n)):
                self.pos = self.now_dict_inv[self.now_dict_[t[j + 1]]]
        return stick


def GetPath(start, goal, pred):
    return GetPathRow(start, goal, pred[start])


def GetPathRow(start, goal, pred_row):
    path = []
    i = goal
    while i != start and i >= 0:
        path.append(i)
        i = pred_row[i]
    if i < 0:
        return []
    path.append(i)
    return path[::-1]
