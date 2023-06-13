"""
exp_lock - 关于线程锁的应用

Author: hanayo
Date： 2023/6/13
"""
import requests
import os
from concurrent.futures import ThreadPoolExecutor
import time
from threading import RLock


class DownloadTool(object):

    def __init__(self, url=""):
        self.index = 0
        self.url = url
        self.lock = RLock()

    def download(self, url):
        resp = requests.get(url)
        filename = url.split("/")[-1]
        if resp.status_code == 200:
            self.lock.acquire()
            self.index += 1
            with open(f"images/beauty/编号{self.index}_{filename}", "wb") as file:
                file.write(resp.content)
            self.lock.release()

    def start(self):
        if not os.path.exists("images/beauty"):
            os.makedirs("images/beauty")
        start = time.time()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)'
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        with ThreadPoolExecutor(max_workers=16) as pool:
            for i in range(3):
                url = f"https://image.so.com/zjl?sn={i * 30}&ch=beauty"
                resp = requests.get(url=url, headers=headers)
                pic_list = resp.json()["list"]
                for pic in pic_list:
                    pool.submit(self.download, url=pic["qhimg_url"])

        end = time.time()
        print(f"多线程下载共耗时：{end - start:.3f}秒")


if __name__ == '__main__':
    DownloadTool().start()

