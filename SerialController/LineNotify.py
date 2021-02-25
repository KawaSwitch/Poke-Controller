import configparser
import cv2
import io
import os

import requests
from PIL import Image


class Line_Notify:

    def __init__(self, camera=None, token_name='token'):
        self.res = None
        self.token_file = configparser.ConfigParser()
        self.open_file_with_utf8()
        self.camera = camera
        self.line_notify_token = self.token_file['LINE'][token_name]
        self.headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        self.chk_token = requests.get('https://notify-api.line.me/api/status', headers=self.headers)
        self.res = self.chk_token
        self.status = self.chk_token.status_code
        self.chk_token_json = self.chk_token.json()

    def open_file_with_utf8(self):
        """
        utf-8 のファイルを BOM ありかどうかを自動判定して読み込む
        """
        is_with_bom = self.is_utf8_file_with_bom(os.path.dirname(__file__) + '\\line_token.ini')

        encoding = 'utf-8-sig' if is_with_bom else 'utf-8'

        self.token_file.read(os.path.dirname(__file__) + '\\line_token.ini', encoding)

    def is_utf8_file_with_bom(self, filename):
        """
        utf-8 ファイルが BOM ありかどうかを判定する
        """
        line_first = open(filename, encoding='utf-8').readline()
        return line_first[0] == '\ufeff'

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
        self.res = requests.post(line_notify_api, headers=headers, data=data)
        if self.res.status_code == 200:
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
        self.res = requests.post(line_notify_api, headers=headers, params=data, files=files)
        if self.res.status_code == 200:
            print("[LINE]テキストと画像を送信しました。")
        else:
            print("[LINE]テキストと画像の送信に失敗しました。")

    def getRateLimit(self):
        try:
            print('X-RateLimit-Limit: ' + self.res.headers['X-RateLimit-Limit'])
            print('X-RateLimit-ImageLimit: ' + self.res.headers['X-RateLimit-ImageLimit'])
            print('X-RateLimit-Remaining: ' + self.res.headers['X-RateLimit-Remaining'])
            print('X-RateLimit-ImageRemaining: ' + self.res.headers['X-RateLimit-ImageRemaining'])
            import datetime
            dt = datetime.datetime.fromtimestamp(int(self.res.headers['X-RateLimit-Reset']),
                                                 datetime.timezone(datetime.timedelta(hours=9)))
            print(dt)
        except AttributeError:
            pass


if __name__ == "__main__":
    '''
    status  HTTPステータスコードに準拠した値
       200  成功時
       401  アクセストークンが無効
    '''
    LINE = Line_Notify()
    print(LINE)
    LINE.getRateLimit()
