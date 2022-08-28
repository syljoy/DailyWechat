# -*- coding: utf-8 -*-
#
# @Email   : syljoy@163.com
# @Github  : https://github.com/syljoy
# @Desc    : 提醒喝水

import os
import random
import requests
from datetime import datetime, timedelta
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import time


app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_DRINK_ID"]

running_time = os.environ["RUNNING_TIME"]
reminder_times = os.environ["REMINDER_TIMES"]
drink_words = os.environ["DRINK_WORDS"]


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_now_time():
    now_ = datetime.now() + timedelta(hours=8)
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return "{}  {}".format(now_.strftime('%Y年%m月%d日 %H:%M'), week_list[now_.weekday()])


data = {}

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

while True:
    # 获取当前时间
    now_time = datetime.now() + timedelta(hours=8)
    print(now_time.strftime('%H:%M'))

    if running_time < now_time.strftime('%H:%M'):
        data['now'] = {"value": get_now_time(), "color": get_random_color()}
        data['times'] = {"value": reminder_times, "color": get_random_color()}
        data['words'] = {"value": drink_words, "color": get_random_color()}
        data['chp'] = {"value": get_words(), "color": get_random_color()}

        count = 0
        for user_id in user_ids:
            res = wm.send_template(user_id, template_id, data)
            count += 1
        print("发送了" + str(count) + "条消息")
        for k, v in data.items():
            v.pop('color', None)
        print(data)

        break
    else:
        time.sleep(1200)

