import _thread,datetime,time
import logging
import os.path

import requests
from flask import Flask, request, json, render_template, make_response, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import log
from message.send import Message
from version import APP_VERSION
login_manager = LoginManager()
login_manager.login_view = "login"


def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# Flask实例
def create_flask_app(config):
    app_cfg = config.get_config('app') or {}
    admin_user = app_cfg.get('login_user') or "admin"
    admin_password = app_cfg.get('login_password') or "password"
    USERS = [{
        "id": 1,
        "name": admin_user,
        "password": generate_password_hash(str(admin_password))
    }]

    App = Flask(__name__)
    App.config['JSON_AS_ASCII'] = False
    App.secret_key = 'jxxghp'
    applog = logging.getLogger('werkzeug')
    applog.setLevel(logging.ERROR)
    login_manager.init_app(App)

    @App.after_request
    def add_header(r):
        r.headers["Cache-Control"] = "no-cache, no-store, max-age=0"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        return r

    # 根据用户名获得用户记录
    def get_user(user_name):
        for user in USERS:
            if user.get("name") == user_name:
                return user
        return None

    # 用户类
    class User(UserMixin):
        def __init__(self, user):
            self.username = user.get('name')
            self.password_hash = user.get('password')
            self.id = 1

        # 密码验证
        def verify_password(self, password):
            if self.password_hash is None:
                return False
            return check_password_hash(self.password_hash, password)

        # 获取用户ID
        def get_id(self):
            return self.id

        # 根据用户ID获取用户实体，为 login_user 方法提供支持
        @staticmethod
        def get(user_id):
            if not user_id:
                return None
            for user in USERS:
                if user.get('id') == user_id:
                    return User(user)
            return None

    # 定义获取登录用户的方法
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @App.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html", error=error), 404

    @App.errorhandler(500)
    def page_server_error(error):
        return render_template("500.html", error=error), 500

    # 主页面
    @App.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            GoPage = request.args.get("next") or ""
            if GoPage.startswith('/'):
                GoPage = GoPage[1:]
            user_info = session.get('_user_id')
            if not user_info:
                return render_template('login.html',
                                       GoPage=GoPage)
            else:
                return render_template('navigation.html',
                                       GoPage=GoPage,
                                       UserName=admin_user,
                                       AppVersion=APP_VERSION)
        else:
            GoPage = request.form.get('next') or ""
            if GoPage.startswith('/'):
                GoPage = GoPage[1:]
            username = request.form.get('username')
            if not username:
                return render_template('login.html',
                                       GoPage=GoPage,
                                       err_msg="请输入用户名")
            password = request.form.get('password')
            user_info = get_user(username)
            if not user_info:
                return render_template('login.html',
                                       GoPage=GoPage,
                                       err_msg="用户名或密码错误")
            # 创建用户实体
            user = User(user_info)
            # 校验密码
            if user.verify_password(password):
                # 创建用户 Session
                login_user(user)
                return render_template('navigation.html',
                                       GoPage=GoPage,
                                       UserName=admin_user,
                                       AppVersion=APP_VERSION)
            else:
                return render_template('login.html',
                                       GoPage=GoPage,
                                       err_msg="用户名或密码错误")

    # gotify 消息接收转发服务
    @App.route("/message", methods=['POST','GET'])
    def message():
        id = 1
        result = ""
        try:
            token = request.args.get('token')
            title = request.form.get("title")
            message = request.form.get("message")
            priority = request.form.get("priority")
            if title == None and message == None:
                my_json = request.get_json()
                title, message, priority = my_json['title'], my_json['message'], my_json['priority']
            date = "{0}{1}".format(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),"+08:00")
            print('{0} message 接口收到 POST 请求，参数：{1}，内容：{2}'.format(getTime(), request.args,
                                                                  {"title": title, "message": message,
                                                                   "priority": priority}))
            result = {
                "id": id,
                "appid": 1,
                "message": message,
                "title": title,
                "priority": priority,
                "date": date
            }
            print('{0} message 接口返回，内容：{1}'.format(getTime(), result))
            Message().sendmsg(token,title,message)
        except Exception as e:
            print("报错",e)
            Message().sendmsg(token, '接收消息处理异常', e)
        return jsonify(result)

    return App