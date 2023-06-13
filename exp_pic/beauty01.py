"""
beauty01 - 采用单线程方式下载90张美女图片

Author: hanayo
Date： 2023/6/13
"""

import requests
import os
import time


def download_pic(url):
    resp = requests.get(url)
    filename = url.split("/")[-1]
    if resp.status_code == 200:
        with open(f"images/beauty/{filename}", "wb") as file:
            file.write(resp.content)


def main():
    if not os.path.exists("images/beauty"):
        os.makedirs("images/beauty")
    start = time.time()
    for i in range(3):
        url = f"https://image.so.com/zjl?sn={i*30}&ch=beauty"
        resp = requests.get(url)
        pic_list = resp.json()["list"]
        for pic in pic_list:
            download_pic(pic["qhimg_url"])
    end = time.time()
    print(f"单线程下载共耗时：{end - start:.3f}秒")


if __name__ == '__main__':
    main()


