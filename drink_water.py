# -*- coding: utf-8 -*-
#
# @Email   : syljoy@163.com
# @Github  : https://github.com/syljoy
# @Desc    : 提醒喝水

import os
import random
from datetime import datetime, timedelta

import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import time


app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_DRINK_ID"]


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_now_time():
    now_time = datetime.now() + timedelta(hours=8)
    now_time = datetime.now()
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return "{}  {}".format(now_time.strftime('%Y年%m月%d日 %H:%M'), week_list[now_time.weekday()])


def get_word_drink(index=0):
    drink_words = ["养成健康喝水好习惯，做健康好宝宝。",
                   "起床之际要喝水，起到排毒养颜的所用。",
                   "清晨到起床到办公室后要喝水，补充水分，缓解紧张情绪。",
                   "工作一段时间后喝第三杯水，解乏放松，缓解工作压力。",
                   "用完午餐半个小时后喝水，加强消化功能，减负又减肥。",
                   "下午茶时间到了，一杯水能够提神醒脑。",
                   "下班离开办公室前喝一杯水，晚餐不会暴饮暴食。",
                   "用完晚餐半小时后喝水，加强消化功能，减负又减肥。",
                   "睡前1至半小时喝适量水，有助于新陈代谢和安神睡眠。"]
    return drink_words[index]
times = 0
data = {
    "now": {"value": get_now_time(), "color": get_random_color()},
    "words": {"value": get_word_drink(0), "color": get_random_color()},
    "times": {"value": times, "color": get_random_color()},
    "chp": {"value": get_words(), "color": get_random_color()},
}

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

while True:

    # 更新信息是否已发送
    is_sending = True
    # 获取当前时间 - 差了8个时区
    now_time = datetime.now() + timedelta(hours=8)
    print(now_time.strftime('%H:%M'))
    if "22:00" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(8)
        is_sending = False
        break
    elif "19:00" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(7)
        is_sending = False
    elif "17:20" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(6)
        is_sending = False
    elif "15:00" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(5)
        is_sending = False
    elif "12:20" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(4)
        is_sending = False
    elif "10:40" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(3)
        is_sending = False
    elif "08:20" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(2)
        is_sending = False
    elif "07:00" < now_time.strftime('%H:%M'):
        data['words']['value'] = get_word_drink(1)
        is_sending = False
    else:
        pass
    if not is_sending:
        times = times + 1
        data['times']['value'] = times
        count = 0
        for user_id in user_ids:
            res = wm.send_template(user_id, template_id, data)
            count += 1
        print("发送了" + str(count) + "条消息")
        for k, v in data.items():
            v.pop('color', None)
        print(data)
        is_sending = True

    time.sleep(1200)




