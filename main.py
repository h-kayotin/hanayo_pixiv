"""
main - 爬虫实践之pixiv

Author: hanayo
Date： 2023/6/12
"""

import requests

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'Cookie': '你的cookie'
}

res = requests.get("https://www.pixiv.net", headers=headers)
print(res.text)