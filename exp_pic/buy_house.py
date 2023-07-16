"""
buy_house - 爬取贝壳网二手房数据

Author: kayotin
Date 2023/7/16
"""
import os
import datetime
import requests
from bs4 import BeautifulSoup
import json


class ShellSpider:

    city_names = {
        "sh": "上海",
        "gz": "广州"
    }

    def __init__(self, name, city="sh"):
        self.name = name
        self.city = city
        self.city_cn = ShellSpider.city_names[self.city]
        self.date_string = datetime.date.today()
        self.city_url = f"https://{self.city}.ke.com/ershoufang/"
        self.check_folder()
        self.areas = list()

    def __str__(self):
        return f"开始爬取来自{self.name}的{self.city_cn}的二手房数据，今天是{self.date_string}。"

    def check_folder(self):
        """导出文件夹是否存在"""
        folder_name = f"datas/house/{self.city_cn}{self.date_string}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def get_areas(self):
        """获取一个城市所有的区域"""
        # https://sh.ke.com/ershoufang/
        resp = requests.get(self.city_url)
        bs_html = BeautifulSoup(resp.content, "html.parser")
        links_items = bs_html.find_all("a", {"class": "CLICKDATA",
                                          "data-action": "source_type=PC小区列表筛选条件点击"})
        for item in links_items:
            area = {
                "name_cn": item.text,
                "url": f"https://sh.ke.com/{item.get('href')}"
            }
            self.areas.append(area)


        # page = f'http://{self.city}.ke.com/ershoufang/{2}/'

    def get_pages_by_area(self):
        """根据各个区域，获取共有多少页"""
        for area in self.areas:
            url = area["url"]
            resp = requests.get(url)
            bs_html = BeautifulSoup(resp.content, "html.parser")
            pages = bs_html.find_all("div", {
                "class": "page-box house-lst-page-box",
                "comp-module": "page"
            })
            # print(pages)
            page_dict = json.loads(pages[0].get("page-data"))
            area["pages"] = page_dict["totalPage"]

    def start(self):
        """根据每页的链接，来进行爬取"""
        self.get_areas()

    def save_data(self):
        """把爬取到的数据，保存到excel"""


if __name__ == '__main__':
    my_spider = ShellSpider("shell")
    print(my_spider)
    my_spider.get_areas()
    my_spider.get_pages_by_area()
    print(my_spider.areas)

