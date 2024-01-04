"""
movie_hana - 

Author: kayotin
Date 2024/1/4
"""

import re
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.87 Safari/537.36',
    'Referer': 'https://tfz.maoyan.com/'
}


class MovieSpider(object):

    def __init__(self):
        self.host = "https://www.maoyan.com/"
        self.url = "https://www.maoyan.com/films?showType=3&yearId=13&sortId=3&offset="
        self.length = 60
        self.pg_size = 30
        self.headers = header
        self.detail_url_list = []

    def get_detail_url(self):
        for i in range(0, self.length, self.pg_size):
            pg_url = f"{self.url}{i}"
            headers = self.headers
            resp_html = requests.get(pg_url, headers=headers).text
            soup_html = BeautifulSoup(resp_html.replace("&#x", ""), 'lxml')

            # 所有电影标签是放在dd这个标签里的，所以获取dd就行了
            dd_list = soup_html.find_all('div', {'class': 'channel-detail movie-item-title'})
            print(len(dd_list))
            for div in dd_list:
                link = div.find("a")
                if link is not None:
                    detail_url = f"{self.host}{link}"
                    self.detail_url_list.append(detail_url)
        for s in self.detail_url_list:
            print(s)


if __name__ == '__main__':
    my_spider = MovieSpider()
    my_spider.get_detail_url()