from flask import Flask,request,jsonify
import os,base64,time,json,requests,datetime,urllib3

def send2bark(token,title,message,groupName,soundName='telegraph',iconUrl='',url='',barkUrl=''):
    try:
        response = requests.post(
            url = "{0}/push".format(barkUrl),
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "body": message,
                "device_key": token,
                "title": title,
                "category": "category",
                "sound": soundName,
                "badge": 1,
                "icon": iconUrl,
                "group": groupName,
                "url": url
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def gotifyMessage(msg):
    return msg

app = Flask(__name__)

@app.route("/message",methods=['POST'])
def message():
    global id,bark_token,soundName,barkUrl
    id += 1
    try:
        title = request.form.get("title")
        message = request.form.get("message")
        priority = request.form.get("priority")
        if title == None and message == None:
            my_json = request.get_json()
            title,message,priority = my_json['title'],my_json['message'],my_json['priority']
        date = "{0}{1}".format(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),"+08:00")
        print('{0} message 接口收到 POST 请求，参数：{1}，内容：{2}'.format(getTime(),request.args,{"title":title,"message":message,"priority": priority}))
        result = {
            "id": id,
            "appid": 1,
            "message": message,
            "title": title,
            "priority": priority,
            "date": date
        }
        # print('{0} message 接口返回，内容：{1}'.format(getTime(), result))
        send2bark(barkUrl=barkUrl,token=bark_token,title=title,message=message,groupName='watchtower',soundName=soundName,iconUrl='https://s1.ax1x.com/2022/05/01/OCm3L9.png')
    except Exception as e:
        send2bark(token=bark_token,title='接收消息处理异常',message=e,groupName='watchtower',soundName=soundName,iconUrl='https://s1.ax1x.com/2022/05/01/OCm3L9.png')
    return jsonify(result)


if __name__=="__main__":
    id = 0
    bark_token = 'AmGnn9WZSJKfcsCcjDYnim'
    soundName = 'telegraph'
    barkUrl = 'https://api.day.app'
    # https方式
    # app.run(host="192.168.2.205", debug=True, port=443, ssl_context='adhoc')

    # http方式
    app.run(host="0.0.0.0", debug=False, port=80)
