'''
This code has copied from https://qiita.com/Esfahan/items/275b0f124369ccf8cf18
'''

# -*- coding:utf-8 -*-
from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG
import logging

mapping = {
    "TRACE": " trace ]",
    "DEBUG": " \x1b[0;36mdebug\x1b[0m ",
    "INFO": "  \x1b[0;32minfo\x1b[0m ",
    "WARNING": "  \x1b[0;33mwarn\x1b[0m ",
    "WARN": "  \x1b0;33mwarn\x1b[0m ",
    "ERROR": "\x1b[0;31m error \x1b[0m",
    "ALERT": "\x1b[0;37;41m alert \x1b[0m",
    "CRITICAL": "\x1b[0;37;41m alert \x1b[0m",
}


class ColorfulHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> None:
        record.levelname = mapping[record.levelname]
        super().emit(record)


def root_logger():
    # logging.basicConfig(handlers=[ColorfulHandler()], level=logging.DEBUG)
    # root loggerを取得
    logger = getLogger()

    # formatterを作成
    formatter = Formatter('%(asctime)s %(name)s %(funcName)s [%(levelname)s]: %(message)s')

    # handlerを作成しフォーマッターを設定
    # handler = ColorfulHandler()
    handler = StreamHandler()
    handler.setFormatter(formatter)

    # loggerにhandlerを設定、イベント捕捉のためのレベルを設定
    logger.addHandler(handler)
    # log levelを設定
    logger.setLevel(DEBUG)
    # logger.debug("hello")
    # logger.info("hello")
    # logger.warning("hello")
    # logger.error("hello")
    # logger.critical("hello")

    return logger
