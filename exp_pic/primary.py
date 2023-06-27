"""
main - 爬虫实践之pixiv 这个可以说是一步一步试的过程了

Author: hanayo
Date： 2023/6/12
"""

import requests
from static.config import cookie, agent

headers = {
    'User-Agent': agent,
    'Cookie': cookie
}

rank_male_url = "https://www.pixiv.net/ranking.php?mode=male&p=1&format=json"

weekly_url = "https://www.pixiv.net/ranking.php?mode=weekly&p=1&format=json"
res = requests.get(weekly_url, headers=headers)
datas = res.json()["contents"]
images_list = []
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
# 获取第一张图片
image_1 = images_list[0]
# 通过以下链接，请求图片详情
image_url = f"https://www.pixiv.net/ajax/illust/{image_1['p_id']}/pages?lang=zh"
resp_image = requests.get(image_url, headers=headers)
# 数据保存在body字段
image_data = resp_image.json()["body"]
# 因为图片可能有多p，所以是一个列表。我们拿第一个的urls字段，其中的original就是原图
download_url = image_data[0]["urls"]["original"]
download_headers = headers
# 如果不加referer字段，直接请求下载链接p站不给结果
download_headers["referer"] = image_1["referer"]
# 通过如下请求，我们获得了最终的下载链接
resp_final = requests.get(download_url, headers=download_headers)
file_name = download_url.split(".")[-1]
with open(f"output/{image_1['p_id']}.{file_name}", "wb") as file:
    file.write(resp_final.content)
