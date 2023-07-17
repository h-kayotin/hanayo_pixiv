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
from concurrent.futures import ThreadPoolExecutor


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
        print(f"正在获取{self.city_cn}的所有行政区信息-->", end="")
        resp = requests.get(self.city_url)
        bs_html = BeautifulSoup(resp.content, "html.parser")
        links_items = bs_html.find_all("a", {"class": "CLICKDATA",
                                          "data-action": "source_type=PC小区列表筛选条件点击"})
        for item in links_items:
            area = {
                "name_cn": item.text,
                "url": f"https://sh.ke.com/{item.get('href')}",
                "towns": [
                    # {
                    #     "name": "北蔡",
                    #     "url": "...",
                    #     "page_num": ""
                    # }
                ]
            }
            self.areas.append(area)
        print(f"{self.city_cn}的{len(self.areas)}个区的信息已获取完毕。\n")

    @staticmethod
    def get_towns(url, area):
        """获取每个区下面有几个镇，比如普陀区真如板块"""
        bs_html = ShellSpider.get_bs_html(url)
        divs = bs_html.find_all("div", {"data-role": "ershoufang"})
        items = divs[0].find_all("a", {"class": ""})
        for item in items:
            town = {
                "name": item.text,
                "url": f"https://sh.ke.com/{item.get('href')}"
            }
            area["towns"].append(town)

    @staticmethod
    def get_bs_html(url):
        """这两句反复用到，所以作成个方法了"""
        resp = requests.get(url)
        bs_html = BeautifulSoup(resp.content, "html.parser")
        return bs_html

    @staticmethod
    def get_page_num(url, town):
        """获取共有多少页"""
        bs_html = ShellSpider.get_bs_html(url)
        pages = bs_html.find_all("div", {
            "class": "page-box house-lst-page-box",
            "comp-module": "page"
        })
        page_dict = json.loads(pages[0].get("page-data"))
        town["page_num"] = page_dict["totalPage"]

    def get_towns_by_area(self):
        """根据各个区域，获取共有多少镇"""
        print("正在获取各行政区下属的街道-->", end="")
        town_total = 0
        with ThreadPoolExecutor(max_workers=16) as pool:
            for area in self.areas:
                pool.submit(ShellSpider.get_towns, url=area["url"], area=area)
        for area in self.areas:
            town_total += len(area["towns"])
        print(f"街道数量共有{town_total}个获取完毕。\n")

    def get_pages_by_town(self):
        print("开始读取各街道的房源页数-->", end="")
        with ThreadPoolExecutor(max_workers=50) as pool:
            for area in self.areas:
                for town in area["towns"]:
                    pool.submit(ShellSpider.get_page_num, url=town["url"], town=town)
        print("页数读取完毕。\n")

    def start(self):
        """根据每页的链接，来进行爬取"""
        self.get_areas()
        self.get_towns_by_area()
        self.get_pages_by_town()

    def save_data(self):
        """把爬取到的数据，保存到excel"""
        pass


if __name__ == '__main__':
    my_spider = ShellSpider("shell")
    my_spider.start()
    print(my_spider.areas)

