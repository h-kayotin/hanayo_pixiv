"""
test - 

Author: kayotin
Date 2023/7/16
"""
import requests
from bs4 import BeautifulSoup
import json

url = "https://sh.ke.com/ershoufang/beicai/"
resp = requests.get(url)
bs_html = BeautifulSoup(resp.content, "html.parser")
pages = bs_html.find_all("div", {
    "class": "page-box house-lst-page-box",
    "comp-module": "page"
})
page_dict = json.loads(pages[0].get("page-data"))
print(page_dict["totalPage"])
