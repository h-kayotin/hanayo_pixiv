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
import pandas as pd
import re
from threading import RLock
import time
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.types import NVARCHAR, FLOAT, DATE, Integer


def fmt_info(src_info):
    """格式化一下获取到的房子信息，去掉换行和空格"""
    info = str(src_info).replace("\n", "").replace(" ", "")
    return info


def fmt_price(price):
    """将带单位的数字，转换成浮点型数字"""
    # 首先去掉逗号
    string_num = re.sub(r',', '', price)

    # 使用正则表达式提取数字
    number = re.findall(r'\d+', string_num)[0]

    # 将提取的数字转换为float类型
    float_num = float(number)
    return float_num


class ShellSpider:
    # 如需其他城市，请先在这添加城市代码
    city_names = {
        "sh": "上海",
        "gz": "广州"
    }
    columns = ["行政区", "街道", "小区", "房屋信息", "总价（万元）", "单价（元）"]
    house_info_df = pd.DataFrame(columns=columns, index=range(0))
    lock = RLock()

    def __init__(self, name, city="sh", mysql=False):
        self.name = name
        self.city = city
        self.city_cn = ShellSpider.city_names[self.city]
        self.date_string = datetime.date.today()
        self.city_url = f"https://{self.city}.ke.com/ershoufang/"
        self.save_path = self.check_folder()
        self.areas = list()
        self.excel_name = f"{self.save_path}/房价数据.xlsx"
        self.is_mysql = mysql

    def __str__(self):
        return f"开始爬取来自{self.name}的{self.city_cn}的二手房数据，今天是{self.date_string}。"

    def check_folder(self):
        """导出文件夹是否存在"""
        folder_name = f"datas/house/{self.city_cn}{self.date_string}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

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

    def get_info_by_page(self):
        print("开始根据街道和页数信息获取二手房数据-->")
        with ThreadPoolExecutor(max_workers=50) as pool:
            for area in self.areas:
                for town in area["towns"]:
                    print(f"开始读取{town['name']}的数据-->")
                    for page_num in range(1, town["page_num"] + 1):
                        url = f"{town['url']}pg{page_num}/"
                        pool.submit(ShellSpider.get_info,
                                    url=url, town_name=town["name"],
                                    area_name=area["name_cn"])
        print(f"二手房数据读取完毕。\n")

    @staticmethod
    def get_info(url, town_name, area_name):
        bs_html = ShellSpider.get_bs_html(url)
        info_divs = bs_html.find_all("div", {"class": "info clear"})
        for info_div in info_divs:
            # 分别获取小区名，房屋信息，总价，单价
            community_name = fmt_info(info_div.find('div', class_='positionInfo').text)
            house_info = fmt_info(info_div.find('div', class_='houseInfo').text)
            total_price = fmt_info(info_div.find('div', class_='totalPrice totalPrice2').text)
            total_price = fmt_price(total_price)
            unit_price = fmt_info(info_div.find('div', class_='unitPrice').text)
            unit_price = fmt_price(unit_price)
            row = [area_name, town_name, community_name, house_info, total_price, unit_price]
            # 为了防止多个线程同时修改同一行数据导致数据不一致，加上线程锁
            ShellSpider.lock.acquire()
            ShellSpider.house_info_df.loc[len(ShellSpider.house_info_df)] = row
            # 写入后解锁
            ShellSpider.lock.release()
        if len(ShellSpider.house_info_df) % 1000 >= 900:
            print(f"爬虫全力运行中，本次读取了{town_name}的一页数据，当前Dataframe中"
                  f"有{len(ShellSpider.house_info_df)}条数据。")

    def start(self):
        """根据每页的链接，来进行爬取"""
        self.get_areas()
        self.get_towns_by_area()
        self.get_pages_by_town()
        self.get_info_by_page()
        print(f"共获取到{len(self.house_info_df)}条数据。")
        self.save_data()

    def save_data(self):
        """把爬取到的数据，保存到excel"""
        print("开始写入到Excel--->", end="")
        excel_name = f"{self.save_path}/房价数据.xlsx"
        self.house_info_df.to_excel(excel_name, index=True)
        print("写入Excel完毕。\n")

    def save_to_mysql(self):
        """把数据从dataframe存储到mysql数据库里"""
        host = '192.168.32.14'
        user = 'root'
        # 注意这里密码含有@，用%40代替
        passwd = 'abc%401234'
        db = 'house_data'
        port = 3306
        engine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8")
        table_name = f"tb_{self.city}"

        # 加上日期
        self.house_info_df["date"] = self.date_string

        # 指定表字段数据类型
        type_dict = {
            "area": NVARCHAR(length=255),
            "street": NVARCHAR(length=255),
            "community": NVARCHAR(length=255),
            "info": NVARCHAR(length=255),
            "total": FLOAT,
            "unit": FLOAT,
            "date": DATE
        }

        # 指定数据类型，和表已存在，进行append
        self.house_info_df.to_sql(table_name, engine, if_exists='append', index=False, dtype=type_dict)



if __name__ == '__main__':
    start = time.time()
    my_spider = ShellSpider("shell")
    # my_spider = ShellSpider("shell", city="gz", mysql=True)
    print(my_spider)
    # my_spider.start()
    # cost_time = time.time() - start
    # print(f"运行完毕，共耗时{cost_time:.2f}秒。")
    my_spider.house_info_df = pd.read_excel(io="datas/house/上海2023-07-17/房价数据.xlsx", index_col="id")
    my_spider.save_to_mysql()
