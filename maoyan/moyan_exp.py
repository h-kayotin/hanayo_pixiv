"""
moyan_exp - 猫眼破解字体反爬的一个例子

Author: kayotin
Date 2024/1/7
"""

import re
import requests
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
import os
import xml.dom.minidom as xml_dom
from lxml import etree

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
    resp = requests.get(url, headers=header)
    resp_html = resp.text
    print(resp_html)
    e_t = etree.HTML(resp_html)
    font_url = e_t.xpath('/html/head/style/text()')
    print(font_url)


def down_font(url):
    r = requests.get('http://'+url)
    with open("demo.woff", "wb") as code:
        code.write(r.content)
    font = TTFont("demo.woff")
    font.saveXML('to.xml')


def find_star(titles):
    # 加载字体模板
    num = [8, 6, 2, 1, 4, 3, 0, 9, 5, 7]
    data = []
    new_font = []
    xml_file_path_temp = os.path.abspath("temp.xml")
    domo_bj_temp = xml_dom.parse(xml_file_path_temp)
    element_obj_temp = domo_bj_temp.documentElement
    sub_element_obj = element_obj_temp.getElementsByTagName("TTGlyph")
    for i in range(len(sub_element_obj)):
        re_obj = re.compile(r"name=\"(.*)\"")
        find_list = re_obj.findall(str(sub_element_obj[i].toprettyxml()))
        data.append(str(sub_element_obj[i].toprettyxml()).replace(find_list[0], '').replace("\n", ''))

    # 根据字体模板解码本次请求下载的字体
    xml_file_path_find = os.path.abspath("to.xml")
    domo_bj_find = xml_dom.parse(xml_file_path_find)
    element_obj_find = domo_bj_find.documentElement
    t_unicode = element_obj_find.getElementsByTagName("TTGlyph")
    for i in range(len(t_unicode)):
        th = t_unicode[i].toprettyxml()
        report = re.compile(r"name=\"(.*)\"")
        find_this = report.findall(th)
        get_code = th.replace(find_this[0], '').replace("\n", '')
        for j in range(len(data)):
            if not cmp(get_code, data[j]):
                new_font.append(num[j])

    font = TTFont("demo.woff")
    font_list = font.getGlyphNames()
    font_list.remove('glyph00000')
    font_list.remove('x')

    # 匹配
    star_woff = re.findall(re.compile(r">(.*)<"), str(titles[0]))[0].replace(';', '').split('.')
    for i in star_woff:
        get_this = i.upper()
        for j in range(len(font_list)):
            if not cmp(get_this, font_list[j].replace("uni", "")):
                print(new_font[j])





if __name__ == '__main__':
    test_url = 'https://maoyan.com/films/42964'
    get_font_url(test_url)
