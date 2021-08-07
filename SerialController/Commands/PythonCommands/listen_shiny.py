#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

try:
    import pyaudio
except ImportError:
    print("PyAudio is not installed.")
    pass
except:
    pass

import numpy as np
from datetime import datetime

# import matplotlib.pyplot as plt

'''
色違いの音を検出したい
という気持ちを満たす(かもしれない)スクリプトです
実行中にｷﾗｰﾝが鳴ると反応します


事前にswitchの音を何らかの手段でPCに取り込む必要があります．
OpenCVの使用中(=映像キャプチャ中)は他の手段でキャプチャボードの映像を受け取れませんが，
それだけでなく音も受け取れません(OpenCVに音の受け取り機能が存在しない&排他処理みたいなことがされています

このため少し面倒な手順が必要になってきます
以下に，映像を受け取りながらPCのにSwitchの音を入力する方法の例を挙げます．

・キャプチャーボードのパススルー機能で，音声出力機能のついた(ヘッドホン端子のある)モニター/TVとSwitchを接続し，
　そのモニター/TVとPCのマイク端子をオス-オスAUXケーブルで接続する

・Switchのイヤホン端子はTVモードでも使用可能なので，そことPCのマイク端子をオス-オスAUXケーブルで接続する．
　お手軽ですがSwitchに直で接続するため結構ノイズが乗ります(ケーブル次第かもしれません)

・OBSのVirtualCamera機能を利用する．OBSには仮想カメラ機能があり，PokeCon側で認識可能です(ラグは増えます)
　(ただし組み込み版の仮想カメラは不可で，プラグイン版の仮想カメラに限る)
　OBSは受け取った音をPCに接続されている任意のデバイスに出力できるので，その出力先からAUXケーブルなどでPCのマイク端子に接続する
・あるいはOBSからVoicemeeterなどの仮想サウンドデバイスに"入力"することでその出力を受け取る方法もあります．
　この方法であれば追加のケーブルは不要ですが，設定が面倒かもしれません．
'''


class ListenShiny(PythonCommand):
    NAME = '色違いの音を聴きたい'

    def __init__(self):
        super().__init__()

    def do(self):

        CHUNK = 1024
        RATE = 44100
        l = 1e7  # 閾値．入力の音量によって変動します．
        sound_count = 0

        data1 = []
        data2 = []

        freqList = np.fft.fftfreq(int(1.5 * RATE / CHUNK) * CHUNK * 2, d=1.0 / RATE)

        p = pyaudio.PyAudio()

        # 以下のコメントアウトを外すとスクリプト実行時にデバイス一覧がprintされるので，
        # 音を取り込んでいるデバイスを探して，そのindexをinput_device_indexに設定する
        # for index in range(0, p.get_device_count()):
        #     print(p. get_device_info_by_index(index))
        device_index = 1

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,  # 1: モノラル
                        input_device_index=device_index,
                        rate=RATE,
                        frames_per_buffer=CHUNK,
                        input=True,
                        output=False)
        self._logger.debug(f"Connect: {p.get_device_info_by_index(device_index)}")
        try:
            while stream.is_active():  # 無限ループします
                if not self.checkIfAlive():
                    # stop押したらbreak処理
                    break
                for i in range(int(1.5 * RATE / CHUNK)):
                    d = np.frombuffer(stream.read(CHUNK), dtype='int16')
                    if sound_count == 0:
                        data1.append(d)

                    else:
                        data1.append(d)
                        data2.append(d)

                if sound_count >= 1:
                    if sound_count % 2 == 1:
                        data = np.asarray(data1).flatten()
                        fft_data = np.fft.fft(data)
                        data1 = []

                    else:
                        data = np.asarray(data2).flatten()
                        fft_data = np.fft.fft(data)
                        data2 = []

                    fft_abs = np.abs(fft_data)  # / (np.max(fft_data)-np.min(fft_data)) * 1e7
                    # 正規化っぽいことしようと思ったけどよくわからなかった

                    # plt.plot(freqList, fft_abs)  # matplotlibで可視化するとき用．
                    # # plt.xlim(3400, 4500)
                    # plt.draw() #  グラフ表示用
                    # plt.show() #  グラフ表示用

                    data3100 = fft_abs[np.where((freqList < 3200) & (freqList > 3000))]  # 3100Hz付近の周波数成分
                    data4200 = fft_abs[np.where((freqList < 4400) & (freqList > 4150))]  # 4200Hz付近の周波数成分

                    if (data3100.max() > 0.4 * l) and (data4200.max() > 1 * l):
                        # 3100Hz付近と4200Hz付近の強度が一定以上あったとき、色違いと判断
                        # 4200Hz付近のほうが強いので閾値に0.4掛けしています．
                        # スペクトラムを見る限り3100Hzの倍音もなっているような気がするので，それも追加で認識してもよいのかも

                        this_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        # 出会ったときの音を保存したいなら以下のコメントアウトを外す
                        # file_name = this_time + ".wav"
                        #
                        # wf = wave.open(file_name, 'w')
                        # wf.setnchannels(1)
                        # wf.setsampwidth(2)
                        # wf.setframerate(RATE)
                        # wf.writeframes(data)
                        # wf.close()

                        print("Sounds Shiny!" + this_time)
                        self._logger.debug("Recognized sound.")
                        data1 = []
                        data2 = []
                        sound_count = 0

                sound_count += 1

            stream.stop_stream()
            stream.close()
            p.terminate()

        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
