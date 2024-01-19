"""
moyan_exp - 猫眼破解字体反爬的一个例子

Author: kayotin
Date 2024/1/7
"""

import re
import time

import requests
from fontTools.ttLib import TTFont
from lxml import etree
from draw_num_orc import read_num_by_draw
from fontTools.ttLib.woff2 import decompress

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
              'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.maoyan.com',
    'Referer': 'https://maoyan.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/120.0.0.0 Safari/537.36'
}


def get_font_url(url):
    """
    获取加密字体的下载地址
    :param url: 电影请求页面的url
    :return: 返回字体的名称
    """
    resp = requests.get(url, headers=header)
    resp_html = resp.text
    e_t = etree.HTML(resp_html)
    font_str = str(e_t.xpath('/html/head/style/text()'))
    font_file_name = re.findall(r'//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/(\w+\.woff)',
                                font_str)[0]

    return font_file_name


def down_font(font_name):
    """
    下载字体，保存为font.woff font.ttf 和 font.xml
    :param font_name: 字体的名称
    :return:
    """
    font_url = f"//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/{font_name}"
    r = requests.get('http:'+font_url)
    with open(f"font/font.woff", "wb") as code:
        code.write(r.content)
    font = TTFont(f"font/font.woff")
    font.saveXML(f'font/font.xml')
    decompress("font/font.woff", "font/font.ttf")


def get_score(url):
    resp = requests.get(url, headers=header)
    time.sleep(2)
    resp_html = resp.text
    e_t = etree.HTML(resp_html)
    score = e_t.xpath('//span[@class="stonefont"]/text()')[0]
    people_count = e_t.xpath('//span[@class="stonefont"]/text()')[1]
    money = e_t.xpath('//span[@class="stonefont"]/text()')[2]

    print(score)


def main():
    test_url = 'https://maoyan.com/films/42964'
    # font_name = get_font_url(test_url)
    # down_font(font_name)
    # font_dict = read_num_by_draw("font/font.woff")
    # print(font_dict)
    get_score(test_url)


if __name__ == '__main__':
    main()

