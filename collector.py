import requests
import json
from pandas import DataFrame
import time
from pandas import Series
import pandas as pd

headers = {
    'authority': 'member.bilibili.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'dnt': '1',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://member.bilibili.com/v2',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
    # 将****替换为自己的cookie值
    'cookie': "CURRENT_FNVAL=****; _uuid=****; buvid3=****; DedeUserID=****; bili_jct=****; SESSDATA=****",
}

params = (
    ('status', 'is_pubing,pubed,not_pubed'),
    ('pn', '1'),
    ('ps', '10'),
    ('coop', '1'),
    ('interactive', '1'),
)

try:
    time_series = pd.read_pickle('time_series.pkl')
except FileNotFoundError:
    time_series = Series()  # 初始化一个序列，index为time.time()所返回的值，value为该时刻所有视频的数据（DataFrame类型）


while(1):
    print('running...')
    response = requests.get('https://member.bilibili.com/x/web/archives', headers=headers, params=params)

    # print(response.text) #str类型的Jason格式数据
    result = json.loads(response.text)

    together = []  # 将要转换为DataFrame的列表，其中元素为字典
    for i in range(len(result['data']['arc_audits'])):
        t = dict()
        data = result['data']['arc_audits'][i]
        t.update(
            {'AV': data['Archive']['aid'],
             'BV': data['Archive']['bvid'],
             'title': data['Archive']['title'],
             'view': data['stat']['view'],
             'danmu': data['stat']['danmaku'],
             'favourite': data['stat']['favorite'],
             'coin': data['stat']['coin'],
             'share': data['stat']['share'],
             'like': data['stat']['like'],
             'reply': data['stat']['reply']})
        together.append(t)
    df = DataFrame(together)  # 某一时刻的所有视频的数据的DataFrame
    time_series = time_series.append(Series([df], [time.time()]))  # 将该时刻的DataFrame加入时间序列中
    time_series.to_pickle('time_series.pkl')  # 保存时间序列
    time.sleep(1800)  # 延迟半小时
