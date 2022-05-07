import requests,json

from config import Config


class Bark:
    __server = None
    __apikey = None

    def __init__(self):
        self.init_config()

    def init_config(self):
        config = Config()
        message = config.get_config('message')
        if message:
            self.__server = message.get('bark', {}).get('server')
            self.__apikey = message.get('bark', {}).get('apikey')
            self.__custom = message.get('bark', {}).get('custom', {})


    def get_config(self,token):
        result = {'level':"",'sound':"",'group':"",'icon':"",'url':""}
        try:
            for key,value in self.__custom.items():
                keylist = ['level','sound','group','icon','url']
                if value['token'] == token:
                    for item in keylist:
                        result[item] = value[item]
            return True, result
        except Exception as msg_e:
            return False, str(msg_e)

    # 发送Bark消息
    def send_bark_msg(self, token, title, text=""):
        if not title and not text:
            return -1, "标题和内容不能同时为空"
        try:
            if not self.__server or not self.__apikey:
                return False, "参数未配置"
            custom_cfg = self.get_config(token)
            print(custom_cfg)
            if custom_cfg[0] == True:
                custom_cfg = custom_cfg[1]
                res = requests.post(
                    url="{0}/push".format(self.__server),
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=json.dumps({
                        "body": text,
                        "device_key": self.__apikey,
                        "title": title,
                        "category": "category",
                        "level": (custom_cfg['level']),
                        "sound": (custom_cfg['sound'] if custom_cfg['sound'] else "telegraph"),
                        "badge": 1,
                        "icon": custom_cfg['icon'],
                        "group": (custom_cfg['group'] if custom_cfg['group'] else "默认"),
                        "url": (custom_cfg['url'] if custom_cfg['url'] else "")
                    }),
                    timeout=10
                )
                log.info("【MSG】发送{0}消息：title:{1},text:{2},group:{3},icon:{4},url:{5}" % (self.__msg_channel, title, text, custom_cfg['group'], custom_cfg['icon'], custom_cfg['url']))
                if res:
                    ret_json = res.json()
                    code = ret_json['code']
                    message = ret_json['message']
                    if code == 200:
                        return True, message
                    else:
                        return False, message
                else:
                    return False, "未获取到返回信息"
            else:
                return False,conf[1]
        except Exception as msg_e:
            return False, str(msg_e)

if __name__=="__main__":
    app = Bark()
    app.send_bark_msg("AGZpWR6JbUacKjH","title","msg")