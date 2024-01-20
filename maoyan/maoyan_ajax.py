"""
maoyan_ajax -  模仿猫眼ajax请求得到电影数据

运行js代码： pip install pyexecjs

Author: kayotin
Date 2024/1/20
"""

import execjs
import hashlib
import requests

with open(file='js/maoyan.js', mode='r', encoding='utf-8') as f:
    js = f.read()
ctx = execjs.compile(js)
flag = {
    'method': 'GET',
    'channelId': 40011,
    'sVersion': 1,
    'type': 'object'
}
n = ctx.call('getMD5Sign', flag)

e = n['randomNum']
i = n['timeStamp']
o = n['md5sign']
c = n['channelId']
s = n['sVersion']

params = {
    'index': e,
    'timeStamp': i,
    'signKey': o,
    'channelId': c,
    'sVersion': s,
    'webdriver': 'false'
}


header = {
    # 'Accept': '*/*',
    # 'Connection': 'keep-alive',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Host': 'www.maoyan.com',
    # 'Referer': 'https://www.maoyan.com/films/1458876',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # 'X-Requested-With': 'XMLHttpRequest'
}


def get_detail(film_id):
    url = f"https://www.maoyan.com/ajax/films/{film_id}"
    resp = requests.get(url, headers=header, params=params)
    print(resp.status_code)
    print(resp.text)
    # e_t = etree.HTML(resp_html)
    # score = e_t.xpath('//span[@class="stonefont"]/text()')[0]
    # people_count = e_t.xpath('//span[@class="stonefont"]/text()')[1]
    # money = e_t.xpath('//span[@class="stonefont"]/text()')[2]
    #
    # print(score)


if __name__ == '__main__':
    get_detail(1458876)

