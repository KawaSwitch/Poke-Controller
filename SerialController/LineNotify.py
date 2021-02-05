import configparser
import cv2
import io
import os

import requests
from PIL import Image


class Line_Notify:

    def __init__(self, camera=None):
        token_file = configparser.ConfigParser()
        token_file.read(os.path.dirname(__file__) + '\\line_token.ini', 'UTF-8')
        self.camera = camera
        self.line_notify_token = token_file['LINE']['token']
        self.headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        self.chk_token = requests.get('https://notify-api.line.me/api/status', headers=self.headers)
        self.status = self.chk_token.status_code
        self.chk_token_json = self.chk_token.json()

    def __str__(self):
        if self.status == 401:
            return "LINE Token Check FAILED."
        elif self.status == 200:
            return "LINE-Token Check OK!"

    def send_text(self, notification_message):
        """
        LINEにテキストを通知する
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'Message': f'{notification_message}'}
        res = requests.post(line_notify_api, headers=headers, data=data)
        if res.status_code == 200:
            print("[LINE]テキストを送信しました。")
        else:
            print("[LINE]テキストの送信に失敗しました。")

    def send_text_n_image(self, notification_message):
        """
        カメラが開いていないときはテキストのみを通知し、
        開いているときはテキストと画像を通知する
        """
        if self.camera is None:
            print("Camera is not Opened. Send text only.")
            self.send_text(notification_message)
            return

        image_bgr = self.camera.readFrame()
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image_rgb)
        png = io.BytesIO()  # 空のio.BytesIOオブジェクトを用意
        image.save(png, format='png')  # 空のio.BytesIOオブジェクトにpngファイルとして書き込み
        b_frame = png.getvalue()  # io.BytesIOオブジェクトをbytes形式で読みとり

        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'Message': f'{notification_message}'}
        files = {'imageFile': b_frame}
        res = requests.post(line_notify_api, headers=headers, params=data, files=files)
        if res.status_code == 200:
            print("[LINE]テキストと画像を送信しました。")
        else:
            print("[LINE]テキストと画像の送信に失敗しました。")


if __name__ == "__main__":
    '''
    status  HTTPステータスコードに準拠した値
       200  成功時
       401  アクセストークンが無効
    '''
    LINE = Line_Notify()
