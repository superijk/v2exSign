import requests
import re
import time
import os
taskName = 'v2ex签到'

def send(taskName, logText, flag):
    # 获取当前时间的时间戳
    current_timestamp = time.time()

    # 将时间戳转换为本地时间的struct_time对象
    local_time = time.localtime(current_timestamp)

    # 使用strftime()方法将struct_time对象格式化为指定的时间字符串
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

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
        print('今日已签到')
        send(taskName,'今日已签到',True)
except Exception as e:
    print('执行异常 ', e)
    send(taskName,'签到异常',False)



