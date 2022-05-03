import os

import log
from config import Config
from version import APP_VERSION
from web.app import FlaskApp



if __name__ == "__main__":
    # 参数
    os.environ['TZ'] = 'Asia/Shanghai'
    log.console("配置文件地址：%s" % os.environ.get('MSG2BARK_CONFIG'))
    log.console('msg2bark 当前版本号：%s' % APP_VERSION)

    # 启动进程
    log.console("开始启动进程...")

    # 启动主WEB服务
    FlaskApp().run_service()