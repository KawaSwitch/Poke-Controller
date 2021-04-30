#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from Commands.Keys import Button, Direction, Hat
from Commands.PythonCommandBase import PythonCommand
# import numpy as np
from scipy.sparse.csgraph import shortest_path  # , floyd_warshall, dijkstra, bellman_ford, johnson
from scipy.sparse import csr_matrix

raid_pass = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
raid_pass_inv = {v: k for k, v in raid_pass.items()}
raid_pass_list = [[8], [2, 4], [1, 3, 5], [2, 6], [1, 5, 7], [2, 4, 6, 8], [3, 5, 9], [4, 8, 0], [7, 5, 9, 0],
                  [8, 6, 0]]


class Move2(PythonCommand):
    NAME = 'キーボード入力2'

    def __init__(self):
        super().__init__()
        self.s = '6104803094'
        self.now_dict = raid_pass_list
        self.now_dict_ = raid_pass
        self.now_dict_inv = raid_pass_inv
        self.graph = None
        self.d = None
        self.p = None
        self.n = None
        self.MakeGraph()
        self.pos = 1  # 初期位置

    def MakeGraph(self):
        # 無向グラフ
        self.n = len(self.now_dict)
        self.graph = [[0] * self.n for _ in range(self.n)]  # 隣接行列
        for i, g_i in enumerate(self.now_dict):
            for j in g_i:
                self.graph[i][j] = 1

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

    def Move(self, t, stick):
        for j in range(len(t) - 1):
            if t[j + 1] in list(range(67, self.n)):
                if not stick:
                    self.press(Button.A, wait=0.1, duration=0.05)
                    stick = True
                self.press(Button.LCLICK, wait=0.03, duration=0.1)
            elif t[j + 1] in [0]:
                self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j] in [0]:
                self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] == 3:
                self.press(Direction.DOWN, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] == -3:
                self.press(Direction.UP, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] == 1:
                self.press(Direction.RIGHT, wait=0.03, duration=0.05)
            elif t[j + 1] - t[j] == -1:
                self.press(Direction.LEFT, wait=0.03, duration=0.05)
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
