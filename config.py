import logging
import os
import shutil
from collections import deque
from threading import Lock
import ruamel.yaml

# import log

# 默认Headers
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
# 日志级别
LOG_LEVEL = logging.INFO
# 定义一个列表用来保存最近的日志，以便查看
LOG_QUEUE = deque(maxlen=200)

lock = Lock()


# @singleton
class Config(object):
    __config = {}
    __config_path = None

    def __init__(self):
        self.__config_path = os.environ.get('MSG2BARK_CONFIG')
        # self.__config_path = "E://Users//AnlakHui//PycharmProjects//pythonProject//Flask//msg2bark//config//config.yaml"
        self.init_config()

    def init_config(self):
        try:
            if not self.__config_path:
                log.console("【ERROR】MSG2BARK_CONFIG 环境变量未设置，程序无法工作，正在退出...")
                quit()
            if not os.path.exists(self.__config_path):
                cfg_tp_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "config.yaml")
                shutil.copy(cfg_tp_path, self.__config_path)
                log.console("【ERROR】config.yaml 配置文件不存在，已将配置文件模板复制到配置目录...")
            with open(self.__config_path, mode='r', encoding='utf-8') as f:
                try:
                    yaml = ruamel.yaml.YAML()
                    self.__config = yaml.load(f)
                except Exception as e:
                    log.console("【ERROR】配置文件 config.yaml 格式出现严重错误！请检查：%s" % str(e))
                    self.__config = {}
        except Exception as err:
            log.console("【ERROR】加载 config.yaml 配置出错：%s" % str(err))
            return False

    def get_proxies(self):
        return self.get_config('app').get("proxies")

    def get_config(self, node=None):
        if not node:
            return self.__config
        return self.__config.get(node, {})

    def save_config(self, new_cfg):
        self.__config = new_cfg
        with open(self.__config_path, mode='w', encoding='utf-8') as f:
            yaml = ruamel.yaml.YAML()
            return yaml.dump(new_cfg, f)

    def get_config_path(self):
        return self.__config_path

if __name__=="__main__":
    app = Config()
    print(app.get_config('message').get('bark').get('apikey'))
    # print(os.environ.get('MSG2BARK_CONFIG'))