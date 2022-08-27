# -*- coding: utf-8 -*-
#
# @Email   : syljoy@163.com
# @Github  : https://github.com/syljoy
# @Desc    :

import os
from datetime import datetime, timedelta
import random
import requests
import xmltodict
import re
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

# 获取环境变量
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_MORNING_ID"]

city = os.environ[""]
begin_date = os.environ["BEGIN_DATE"]
emoji_number = int(os.environ["EMOJI_MORNING_NUMBER"].strip())

# 这里差了8个时区
today = datetime.now() + timedelta(hours=8)


def get_random_color():
    """获取随机颜色"""
    return "#%06x" % random.randint(0, 0xFFFFFF)


def get_random_emoji():
    """获取随机emoji"""
    return random.choice('💘💝💖💗💓💞💕🥰😍🤩😘😚😙💋💌👫💏💑🌹🤵👰✨🎈🎉')


def get_love_count():
    """计算在一起天数"""
    delta = today - datetime.strptime(begin_date, "%Y-%m-%d")
    return delta.days


def get_words():
    """获取一句彩虹屁"""
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_weathers():
    """获取星期、天气、日出日落、生活指数等"""
    weather_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "wthrcdn.etouch.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }
    url = "http://wthrcdn.etouch.cn/WeatherApi?city=" + city
    response = requests.get(url, headers=weather_headers)
    xml_dict = xmltodict.parse(response.text)
    resp = xml_dict['resp']
    today_weather = resp['forecast']['weather'][0]
    week_day = re.findall(r'星期[一二三四五六七天日]', today_weather["date"])[0]
    high_temp = re.findall(r"-*\d+℃", today_weather['high'])[0].strip()
    low_temp = re.findall(r"-*\d+℃", today_weather['low'])[0].strip()
    sunrise_time = resp['sunrise_1'].strip()
    sunset_time = resp['sunset_1'].strip()
    day_type = today_weather['day']['type'].strip()
    night_type = today_weather['night']['type'].strip()
    if day_type != night_type:
        weather = day_type + "转" + night_type
    else:
        weather = day_type
    zhishus = resp['zhishus']['zhishu']
    zhishus_name = list()
    zhishus_value = list()
    zhishus_detail = list()
    for i in range(len(zhishus)):
        if zhishus[i]['name'] in ['穿衣指数', '紫外线强度', '感冒指数']:
            zhishus_name.append(zhishus[i]['name'])
            zhishus_value.append(zhishus[i]['value'])
            zhishus_detail.append(zhishus[i]['detail'])
    return week_day, high_temp, low_temp, weather, sunrise_time, sunset_time, zhishus_name, zhishus_value, zhishus_detail


week, highest, lowest, t_weather, sunrise, sunset, names_zhishu, values_zhishu, details_hishus = get_weathers()

sun_color = get_random_color()
black_color = "#000000"
values_zhishu_color = get_random_color()
details_zhishu_color = get_random_color()

# 添加基本信息
data = {
    "date": {"value": "{}  {}".format(today.strftime('%Y年%m月%d日'), week), "color": black_color},
    "weather": {"value": "{}  {}".format(t_weather, lowest + "~" + highest), "color": get_random_color()},
    "sunrise": {"value": sunrise, "color": sun_color},
    "sunset": {"value": sunset, "color": sun_color},
    "love_days": {"value": get_love_count(), "color": get_random_color()},
    "words": {"value": get_words(), "color": get_random_color()},
}
# 添加生活指数
for index, (name, value, detail) in enumerate(zip(names_zhishu, values_zhishu, details_hishus)):
    data['name_zhishu{}'.format(index)] = {"value": name + "：", "color": black_color}
    data['value_zhishu{}'.format(index)] = {"value": value + "，", "color": values_zhishu_color}
    data['detail_zhishu{}'.format(index)] = {"value": detail + '\n', "color": details_zhishu_color}
# 添加emoji
for i in range(emoji_number):
    data['emoji{}'.format(i)] = {"value": get_random_emoji(), "color": black_color}

# 创建微信
client = WeChatClient(app_id, app_secret)
wechat_message = WeChatMessage(client)
wm = WeChatMessage(client)

# 开始发送消息
count = 0
for user_id in user_ids:
    res = wm.send_template(user_id, template_id, data)
    count += 1

print("发送了" + str(count) + "条消息")
for k, v in data.items():
    v.pop('color', None)
print(data)
