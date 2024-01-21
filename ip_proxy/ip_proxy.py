"""
ip_proxy - 如何使用代理ip

Author: kayotin
Date 2024/1/21
"""

import requests
import random

proxy_list = [
    '111.1.27.85:80', '58.221.40.175:80', '58.221.40.178:80', '61.164.147.242:80', '42.63.65.46:80'
]


def set_proxies(ip_list):
    idx = random.randint(0, len(ip_list)-1)
    proxies = {
        'HTTP': 'http://' + proxy_list[idx],
        'HTTPS': 'http://' + proxy_list[idx],
    }
    return proxies


def main():
    proxies = {
        'http': 'http://175.24.164.254:80',
        'https': 'http://175.24.164.254:80',
    }

    try:
        res = requests.get('https://httpbin.org/get?', proxies=proxies)
        print(res.text)
    except requests.exceptions.ProxyError as e:
        print("连接错误", e.args)


if __name__ == '__main__':
    main()


