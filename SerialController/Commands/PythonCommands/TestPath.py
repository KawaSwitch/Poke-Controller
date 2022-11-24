from os import path
import os
from Commands.PythonCommandBase import ImageProcPythonCommand


def _test_save_capture(command: ImageProcPythonCommand):
    test_cases = [
        # ファイル名のみ
        ("_test", "./Captures/_test.png"),
        # 相対パス ⇒ saveCapture未対応
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
                f"----------\n[FAILURE]\ninput:{test_case[0]}\nexpected:{test_case[1]}\n----------\n")
        else:
            print(
                f"----------\n[SUCCESSED]\ninput:{test_case[0]}\nexpected:{test_case[1]}\n----------\n")
            os.remove(test_case[1])


def _test_is_contain_template(command: ImageProcPythonCommand):
    test_cases = [
        # ファイル名のみ
        ("_test.png", "./Template/_test.png"),
        # 相対パス
        ("_test/_test.png", "./Template/_test/_test.png"),
        # 絶対パス
        (path.join(path.dirname(__file__), "__test.png"),
         path.join(path.dirname(__file__), "__test.png")),
    ]

    for test_case in test_cases:
        try:
            command.isContainTemplate(test_case[0])
            print(
                f"----------\n[SUCCESSED]\ninput:{test_case[0]}\nexpected:{test_case[1]}\n----------\n")
        except:
            print(
                f"----------\n[FAILURE]\ninput:{test_case[0]}\nexpected:{test_case[1]}\n----------\n")
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
