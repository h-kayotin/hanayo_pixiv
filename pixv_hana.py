"""
pixv_hana - 下载周榜-主程序

Author: hanayo
Date： 2023/6/26
"""

import requests
from exp_pic.cookie_p import agent, cookie
from concurrent.futures import ThreadPoolExecutor


class PixivHana(object):

    def __init__(self):
        self.save_path = ""
        self.cookie = cookie
        self.agent = agent
        self.images_list = list()
        self.headers = {}

    def do_work(self):
        self.get_headers()
        self.get_weekly_pids()
        self.get_urls_thread()

    def get_headers(self):
        self.headers ={
            'User-Agent': agent,
            'Cookie': self.cookie
        }

    def get_weekly_pids(self):
        """通过周榜的链接，获取到pid和链接"""
        weekly_url = "https://www.pixiv.net/ranking.php?mode=weekly&p=1&format=json"
        res = requests.get(weekly_url, headers=self.headers)
        datas = res.json()["contents"]
        for data in datas:
            image = {
                "title": data["title"],
                "user_name": data["user_name"],
                "p_id": data["illust_id"],
                "referer": f"https://www.pixiv.net/artworks/{data['illust_id']}",
                "re_url": f"https://www.pixiv.net/ajax/illust/{data['illust_id']}/pages?lang=zh",
                "download_url": []
            }
            self.images_list.append(image)
        print("周榜pid已收集")

    @staticmethod
    def get_download_url(image, url, headers):
        """获取图片下载链接"""
        resp_image = requests.get(url, headers=headers).json()["body"]
        for img in resp_image:
            download_url = img["urls"]["original"]
            image["download_url"].append(download_url)

    def get_urls_thread(self):
        """多线程的获取图片下载链接"""
        with ThreadPoolExecutor(max_workers=16) as pool:
            for image in self.images_list:
                pool.submit(self.get_download_url,
                            image=image,
                            url=image["re_url"],
                            headers=self.headers)
        for image in self.images_list:
            print(image)

    @staticmethod
    def download_pic(url, headers, path, name):
        pass

    def download_thread(self):
        """多线程进行下载"""
        with ThreadPoolExecutor(max_workers=16) as pool:
            for image in self.images_list:
                download_headers = self.headers
                download_headers["referer"] = image["referer"]
                index = 1
                for down_url in image["download_url"]:
                    pic_type = down_url.split(".")[-1]
                    if index > 1:
                        pic_name = f"{image['title']}_{image['user_name']}_{image['p_id']}_.{pic_type}"
                    else:
                        pic_name = f"{image['title']}_{image['user_name']}_{image['p_id']}_.{pic_type}"
                    index += 1
                    pool.submit(self.get_download_url,
                                url=down_url,
                                headers=download_headers,
                                name=pic_name)



if __name__ == '__main__':
    PixivHana().do_work()
