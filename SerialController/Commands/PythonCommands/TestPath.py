from os import path
import os
import shutil
from Commands.PythonCommandBase import ImageProcPythonCommand


def _test_save_capture(command: ImageProcPythonCommand):
    """
    saveCaptureの挙動を確認する

    | 入力           | 期待される挙動                                   |
    | -------------- | ------------------------------------------------ |
    | ファイル名のみ | `./Captures`以下に保存                           |
    | 相対パス       | `./Captures`以下に新規ディレクトリを作成して保存 |
    | 絶対パス       | 指定先に保存                                     |

    Args:
        command (ImageProcPythonCommand): _description_
    """
    test_cases = [
        # ファイル名のみ
        ("_test", "./Captures/_test.png"),
        # 相対パス
        ("_test/_test", "./Captures/_test/_test.png"),
        # 絶対パス
        (path.join(path.dirname(__file__), "_test"),
         path.join(path.dirname(__file__), "_test.png")),
    ]

    for test_case in test_cases:

        if path.exists(test_case[1]):
            os.remove(test_case[1])

        command.camera.saveCapture(test_case[0])
        if not path.exists(test_case[1]):
            print(
                f"----------\n[FAILURE]\ninput: {test_case[0]}\nexpected: {test_case[1]}\n----------\n")
        else:
            print(
                f"----------\n[SUCCESSED]\ninput: {test_case[0]}\nexpected: {test_case[1]}\n----------\n")
            os.remove(test_case[1])


def _test_is_contain_template(command: ImageProcPythonCommand):
    """
    isContainTemplateの挙動を確認する

    | 入力           | 期待される挙動                         |
    | -------------- | -------------------------------------- |
    | ファイル名のみ | `./Template`以下から取得               |
    | 相対パス       | `./Template`以下のディレクトリから取得 |
    | 絶対パス       | 指定先から取得                         |

    Args:
        command (ImageProcPythonCommand): _description_
    """
    test_cases = [
        # ファイル名のみ
        ("_test.png", "./Template/_test.png"),
        # 相対パス
        ("_test/_test.png", "./Template/_test/_test.png"),
        # 絶対パス
        (path.join(path.dirname(__file__), "_test.png"),
         path.join(path.dirname(__file__), "_test.png")),
    ]

    # ダミーのテンプレートを配置
    for test_case in test_cases:
        command.camera.saveCapture("_")
        try:
            os.makedirs(path.dirname(test_case[1]))
        except:
            pass
        shutil.move("./Captures/_.png", test_case[1])

    for test_case in test_cases:
        try:
            command.isContainTemplate(test_case[0])
            print(
                f"----------\n[SUCCESSED]\ninput: {test_case[0]}\nexpected: {test_case[1]}\n----------\n")
        except Exception as e:
            print(
                f"----------\n[FAILURE]\n{str(e)}\ninput: {test_case[0]}\nexpected: {test_case[1]}\n----------\n")
        finally:
            os.remove(test_case[1])
        # ログ目視


class TestPath(ImageProcPythonCommand):

    NAME = "パス指定のテスト"

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        print("\n====================\nsaveCapture\n====================\n")
        _test_save_capture(self)

        print("\n====================\nisContainTemplate\n====================\n")
        _test_is_contain_template(self)
