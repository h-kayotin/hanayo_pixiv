"""
pixv_hana - 下载周榜——主程序

Author: hanayo
Date： 2023/6/26
"""

import requests
from exp_pic.cookie_p import agent


class PixivHana(object):

    def __init__(self):
        self.save_path = ""
        self.cookie = ""
        self.agent = agent
        self.images_list = list()

    def get_weekly_pids(self):
        """通过周榜的链接，获取到pid和链接"""
        weekly_url = "https://www.pixiv.net/ranking.php?mode=weekly&p=1&format=json"
        res = requests.get(weekly_url, headers={
            'User-Agent': agent,
            'Cookie': self.cookie
        })
        datas = res.json()["contents"]
        for data in datas:
            image = {
                "title": data["title"],
                "user_name": data["user_name"],
                "p_id": data["illust_id"],
                "referer": f"https://www.pixiv.net/artworks/{data['illust_id']}"
            }
            self.images_list.append(image)






if __name__ == '__main__':
    PixivHana()