import re

import log
from config import Config
from message.bark import Bark
# from utils.functions import str_filesize
# from utils.types import SearchType


class Message:
    __msg_channel = None
    __webhook_ignore = None
    __domain = None
    wechat = None
    telegram = None
    serverchan = None
    bark = None

    def __init__(self):
        # self.wechat = WeChat()
        # self.telegram = Telegram()
        # self.serverchan = ServerChan()
        self.bark = Bark()
        self.init_config()

    def init_config(self):
        config = Config()
        message = config.get_config('message')
        if message:
            self.__msg_channel = message.get('msg_channel')

    # 通用消息发送
    def sendmsg(self, token, title, text=""):
        # log.info("【MSG】发送%s消息：title=%s, text=%s" % (self.__msg_channel, title, text))
        if self.__msg_channel == "bark":
            return self.bark.send_bark_msg(token, title, text)
        else:
            return None