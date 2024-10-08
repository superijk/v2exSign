import requests
import re
import time
import os
from datetime import datetime
import pytz
taskName = 'v2ex签到'

def send(taskName, logText, flag):

    # 获取当前UTC时间戳
    timestamp = time.time()

    # 将UTC时间戳转换为UTC的datetime对象
    utc_datetime = datetime.utcfromtimestamp(timestamp)

    # 设置东八区时区
    tz = pytz.timezone('Asia/Shanghai')

    # 将UTC时间转换为东八区时间
    local_datetime = utc_datetime.replace(tzinfo=pytz.UTC).astimezone(tz)
    formatted_time = local_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_time)
    s = formatted_time
    url = os.environ["WECHATPUSHURL"]
    data = {
        'msgtype': 'text',
        'text': {
            'content':
                '任务通知\n\n' +
                '任务名称: ' +
                taskName +
                '\n\n' +
                '运行开始时间:\n' +
                s +
                '\n\n' +
                '运行日志: ' +
                logText +
                '\n\n' +
                '任务是否成功: ' + ('✅✅✅' if flag else '❌❌❌'),
        },
    }
    requests.post(url,json=data)


try:
    ck = os.environ["CK"]
    headers = {'Cookie': ck}
    r = requests.get('https://www.v2ex.com/mission/daily', headers=headers)
    html = r.text
    # print(html)
    match = re.findall('once=(\d+)', html)
    if match:
        print('今日未签到')
        once = match[0]
        match = re.findall('已连续登录 (\d+)', html)
        signDay = ''
        if match:
            signDay = match[0]
        print(signDay)
        print(once)
        r = requests.get('https://www.v2ex.com/mission/daily/redeem?once=' + once, headers=headers)
        print(r.text)
        if re.findall('每日登录奖励已领取', r.text):
            print('v2ex今天签到成功')
            send(taskName,'签到成功'+(signDay+1)+'天',True)
        else:
            print('v2ex今天签到失败')
            send(taskName,'签到失败',False)
    else:
        print('今日已签到')
        send(taskName,'今日已签到',True)
except Exception as e:
    print('执行异常 ', e)
    send(taskName,'签到异常',False)



