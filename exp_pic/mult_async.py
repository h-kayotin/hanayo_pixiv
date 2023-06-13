"""
异步IO的方式

Author: hanayo
Date： 2023/6/13
"""

import asyncio, json, os, time, aiohttp, aiofile


async def download_pic(session, url):
    filename = url[url.rfind('/') + 1:]
    async with session.get(url, ssl=False) as resp:
        if resp.status == 200:
            data = await resp.read()
            async with aiofile.async_open(f"images/beauty/{filename}", "wb") as file:
                await file.write(data)


async def fetch_json():
    async with aiohttp.ClientSession() as session:
        for page in range(3):
            url = f"https://image.so.com/zjl?sn={page*30}&ch=beauty"
            async with session.get(url, ssl=False) as resp:
                if resp.status == 200:
                    resp_str = await resp.text()
                    # 将json转换为字典
                    result = json.loads(resp_str)
                    for dic_pic in result["list"]:
                        await download_pic(session, dic_pic["qhimg_url"])


def main():
    if not os.path.exists("images/beauty"):
        os.makedirs("images/beauty")
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_json())
    loop.close()
    end = time.time()
    print(f"异步IO，执行时间{end - start:.3f}秒")


if __name__ == '__main__':
    main()
