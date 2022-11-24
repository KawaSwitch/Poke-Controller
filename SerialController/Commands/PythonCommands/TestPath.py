from os import path
from Commands.PythonCommandBase import ImageProcPythonCommand


class TestCase:
    def __init__(self, input: str, expected: str, ignore: bool = False) -> None:
        self.__input = input
        self.__expected = expected
        self.__ignore = ignore

    @property
    def input(self):
        return self.__input

    @property
    def expected(self):
        return self.__expected

    @property
    def ignore(self):
        return self.__ignore


class TestPath(ImageProcPythonCommand):

    NAME = "パス指定のテスト"

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):

        test_cases = [
            # ファイル名のみ
            TestCase("_test", "./Captures/_test.png"),
            # 相対パス ⇒ saveCapture未対応
            TestCase("_test/_test", "./Captures/_test/_test.png", True),
            # 絶対パス
            TestCase(path.join(path.dirname(__file__), "_test"),
                     path.join(path.dirname(__file__), "_test.png"))
        ]

        print("saveCapture")
        for test_case in test_cases:
            if test_case.ignore:
                continue
            self.camera.saveCapture(test_case.input)
            if not path.exists(test_case.expected):
                print(
                    f"failure\ninput:{test_case.input}\noutput:{test_case.expected}")
                return

        print("isContainTemplate")
        for test_case in test_cases:
            self.isContainTemplate(test_case.input)
            # ログ目視
