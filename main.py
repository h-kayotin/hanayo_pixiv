"""
main - 爬虫实践之pixiv

Author: hanayo
Date： 2023/6/12
"""

import requests
from exp_pic.cookie_p import cookie, agent

headers = {
    'User-Agent': agent,
    'Cookie': cookie
}

rank_male_url = "https://www.pixiv.net/ranking.php?mode=male&p=1&format=json"

weekly_url = "https://www.pixiv.net/ranking.php?mode=weekly&p=1&format=json"
res = requests.get(weekly_url, headers=headers)
datas = res.json()["contents"]
images_list =[]
for data in datas:
    image = {
        "title": data["title"],
        "user_name":data["user_name"],
        "p_id": data["illust_id"],
        "referer": f"https://www.pixiv.net/artworks/{data['illust_id']}"
    }
    images_list.append(image)
# for image in images_list:
#     headers["referer"] = image["referer"]
#     print(headers)
image_1 = images_list[0]
# headers["referer"] = image_1["referer"]
# print(headers)
image_url = f"https://www.pixiv.net/ajax/illust/{image_1['p_id']}/pages?lang=zh"
resp_image = requests.get(image_url, headers=headers)
image_data = resp_image.json()["body"]
# for page in image_data:
#     print(page["urls"]["original"])
download_url = image_data[0]["urls"]["original"]
download_headers = headers
download_headers["referer"] = image_1["referer"]
resp_final = requests.get(download_url, headers=download_headers)
file_name = download_url.split(".")[-1]
with open(f"output/{image_1['p_id']}.{file_name}", "wb") as file:
    file.write(resp_final.content)
