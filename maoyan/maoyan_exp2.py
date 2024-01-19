"""
maoyan_exp2 - 

https://www.maoyan.com/films?showType=3&yearId=13&sortId=3&offset=

Author: kayotin
Date 2024/1/7
"""

from static.config import agent
from lxml import etree
import requests
from time import sleep


def get_html(url):
    """
    进行请求，获取html代码
    :param url:请求地址
    :return:返回resp.text
    """
    headers = {'User-Agent': agent}
    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    sleep(2)
    if resp.status_code == 200:
        resp.encoding = 'uft-8'
        return resp.text
    else:
        return None


def parse_list(html):
    """
    对电影列表进行处理
    :param html: 传递进来电影列表的页面
    :return: 返回一个列表的url
    """
    e_t = etree.HTML(html)
    list_url = [f"https://www.maoyan.com{url}" for url in e_t.xpath('//div[@class="movie-item film-channel"]/a/@href')]
    return list_url


def parse_index(html):
    """

    :param html: 电影信息的html
    :return: 已经提取好的电影信息
    """
    e_t = etree.HTML(html)
    name = e_t.xpath('//h1[@class="name"]/text()')
    en_name = e_t.xpath('//div[@class="ename ellipsis"]/text()')
    movie_type = e_t.xpath('//li[@class="ellipsis"][1]/text()')
    actors = e_t.xpath('//div[@class="celebrity-group"][2]/ul[@class="celebrity-list clearfix"]/li/div[@class="info"]'
                       '/div[@class="name"]/text()')
    actors = fmt_actors(actors)
    return {
        'name': name, 'en_name': en_name, 'movie_type': movie_type, 'actors': actors
    }


def fmt_actors(actors):
    actor_set = set()
    for actor in actors:
        actor_set.add(actor.strip())
    return actor_set


def main():
    page_size = 1
    for page_num in range(page_size):
        s_url = f"https://www.maoyan.com/films?showType=3&yearId=13&sortId=3&offset={30*page_num}"
        list_html = get_html(s_url)
        list_url = parse_list(list_html)
        for url in list_url:
            print(url)
            info_html = get_html(url)
            movie = parse_index(info_html)
            print(movie)


if __name__ == '__main__':
    # main()

    info_html = get_html("https://www.maoyan.com/films/1229214")
    movie = parse_index(info_html)
    print(movie)
