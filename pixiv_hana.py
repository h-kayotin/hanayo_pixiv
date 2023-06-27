"""
pixv_hana - 下载周榜-主程序

Author: hanayo
Date： 2023/6/26
"""

import requests
from static.config import agent, ico_code
from concurrent.futures import ThreadPoolExecutor
from tkinter.filedialog import askdirectory
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
import pathlib
from queue import Queue
from threading import Thread
import base64
import os


class PixivHana(ttk.Frame):

    queue = Queue()
    is_downloading = False

    def __init__(self, master: ttk.Window):

        # 构建图形化界面
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)
        master.title("hanayo_pixiv")

        # 一些搜索需要的属性
        self.cookie = ""
        self.get_cookie()
        self.agent = agent
        self.images_list = list()
        self.headers = {}
        self.download_type = {
            "weekly": "https://www.pixiv.net/ranking.php?mode=weekly&p=1&format=json",
            "daily": "https://www.pixiv.net/ranking.php?p=1&format=json",
            "male": "https://www.pixiv.net/ranking.php?mode=male&p=1&format=json",
            "male_r18": "https://www.pixiv.net/ranking.php?mode=male_r18&p=1&format=json"
        }

        # 默认保存位置，以及默认下载周榜，默认张数
        _path = pathlib.Path().absolute().as_posix()
        default_path = pathlib.Path(f"{_path}/output")
        if not default_path.exists():
            default_path.mkdir()
        self.save_path = ttk.StringVar(value=f"{_path}/output")
        self.type_var = ttk.StringVar(value="weekly")
        self.pages_var = ttk.StringVar(value="10")

        # 创建顶部的Labelframe块
        option_text = "请选择保存路径和下载模式，然后点击开始"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        # 创建下部的界面，选择路径、下载张数、下载类型以及结果表格
        self.path_row()
        self.pages_row()
        self.types_row()
        self.table_area = None
        self.create_table_area()

        # 创建进度条
        self.progressbar = ttk.Progressbar(
            master=self,
            mode=INDETERMINATE,
            style="striped-success"
        )
        self.progressbar.pack(fill=X, expand=YES)

    def get_cookie(self):
        path = pathlib.Path().absolute()
        with open(f"{path}/my_cookie.txt", "r", encoding="utf-8") as file:
            self.cookie = file.read()

    def path_row(self):
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="保存路径", width=10)  # label 文件夹路径
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.save_path)  # 输入框
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(      # 浏览按钮
            master=path_row,
            text="浏览",
            command=self.on_browser,   # 绑定方法，获取路径
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

    def on_browser(self):
        path = askdirectory(title="选择保存路径")
        if path:
            self.save_path.set(path)

    def pages_row(self):
        term_row = ttk.Frame(self.option_lf)
        term_row.pack(fill=X, expand=YES, pady=15)
        term_lbl = ttk.Label(term_row, text="图片数量", width=10)
        term_lbl.pack(side=LEFT, padx=(15, 0))
        term_ent = ttk.Entry(term_row, textvariable=self.pages_var)
        term_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        search_btn = ttk.Button(
            master=term_row,
            text="开始下载",
            command=self.start_work,
            style=OUTLINE,
            width=8
        )
        search_btn.pack(side=LEFT, padx=5)

    def types_row(self):
        type_row = ttk.Frame(self.option_lf)
        type_row.pack(fill=X, expand=YES)
        type_lbl = ttk.Label(type_row, text="下载类型", width=10)
        type_lbl.pack(side=LEFT, padx=(15, 0))

        weekly_opt = ttk.Radiobutton(
            master=type_row,
            text="周榜",
            variable=self.type_var,
            value="weekly"
        )
        weekly_opt.pack(side=LEFT)
        weekly_opt.invoke()

        daily_opt = ttk.Radiobutton(
            master=type_row,
            text="日榜",
            variable=self.type_var,
            value="daily"
        )
        daily_opt.pack(side=LEFT, padx=15)

        male_opt = ttk.Radiobutton(
            master=type_row,
            text="男性向",
            variable=self.type_var,
            value="male"
        )
        male_opt.pack(side=LEFT, padx=15)

        male_r18 = ttk.Radiobutton(
            master=type_row,
            text="R18",
            variable=self.type_var,
            value="male_r18"
        )
        male_r18.pack(side=LEFT, padx=15)

        back_button = ttk.Button(
            master=type_row,
            text="关闭",
            command=self.quit,
            style="success solid toolbutton",
            width=8
        )
        back_button.pack(side=RIGHT, padx=6)

    def create_table_area(self):
        self.table_area = ttk.Treeview(
            master=self,
            style="info",
            columns=["#0", "#1", "#2", "#3", "#4"],  # 列表长度代表列数
            show=HEADINGS
        )
        self.table_area.pack(fill=BOTH, expand=YES, pady=10)

        # setup columns and use `scale_size` to adjust for resolution
        # 初始化列标题，用scale_size去调整列宽
        self.table_area.heading(0, text='标题', anchor=W)
        self.table_area.heading(1, text='作者', anchor=W)
        self.table_area.heading(2, text='Pixiv_ID', anchor=E)
        self.table_area.heading(3, text='下载情况', anchor=E)
        self.table_area.column(
            column=0,
            anchor=W,
            width=utility.scale_size(self, 280),
            stretch=False
        )
        self.table_area.column(
            column=1,
            anchor=W,
            width=utility.scale_size(self, 80),
            stretch=False
        )
        self.table_area.column(
            column=2,
            anchor=E,
            width=utility.scale_size(self, 150),
            stretch=False
        )
        self.table_area.column(
            column=3,
            anchor=E,
            width=utility.scale_size(self, 80),
            stretch=False
        )

    def start_work(self):
        Thread(
            target=self.do_work,
            daemon=True
        ).start()

    def do_work(self):
        # 先清除上一次结果
        self.images_list = []
        items = self.table_area.get_children()
        for item in items:
            self.table_area.delete(item)
        # 开始干活
        self.progressbar.start(10)
        self.get_headers()
        self.get_pids()
        self.get_urls_thread()
        self.download_thread()

    def get_headers(self):
        self.headers = {
            'User-Agent': agent,
            'Cookie': self.cookie
        }

    def get_pids(self):
        """通过周榜的链接，获取到pid和链接"""
        pic_type = self.type_var.get()
        res_url = self.download_type[pic_type]
        res = requests.get(res_url, headers=self.headers)
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
            if len(self.images_list) == int(self.pages_var.get()):
                break
        # print("周榜pid已收集")

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

    @staticmethod
    def download_pic(url, headers, path, name, image, is_last):
        resp = requests.get(url, headers=headers)
        row_info = {
            "title": image["title"],
            "user_name": image["user_name"],
            "p_id": image["p_id"],
            "status": ""
        }
        if resp.status_code == 200:
            row_info["status"] = "下载成功"
            if is_last:
                PixivHana.queue.put(row_info)
            with open(f"{path}/{name}", "wb") as file:
                file.write(resp.content)
        else:
            row_info["status"] = "下载失败"
            PixivHana.queue.put(row_info)

    def download_thread(self):
        """多线程进行下载，多页放一个文件夹"""
        PixivHana.is_downloading = True
        self.after(500, lambda: self.check_queue())
        with ThreadPoolExecutor(max_workers=16) as pool:
            for image in self.images_list:
                download_headers = self.headers
                download_headers["referer"] = image["referer"]
                index = 1
                # 这个变量用来判断多p是否都下载了，下载最后一p才推送入队列
                is_last = False
                for down_url in image["download_url"]:
                    pic_type = down_url.split(".")[-1]
                    save_path = self.save_path.get()
                    if len(image["download_url"]) > 1:
                        dic_name = f"{image['title']}_{image['user_name']}"
                        dic_path = f"{self.save_path.get()}/{dic_name}"
                        dic_path = pathlib.Path(dic_path)
                        if not dic_path.exists():
                            dic_path.mkdir()
                        pic_name = f"p{index}.{pic_type}"
                        save_path = dic_path
                    else:
                        pic_name = f"{image['title']}_{image['user_name']}.{pic_type}"
                    if index == len(image["download_url"]):
                        is_last = True
                    index += 1
                    pool.submit(self.download_pic,
                                url=down_url,
                                headers=download_headers,
                                path=save_path,
                                name=pic_name,
                                image=image,
                                is_last=is_last,
                                )
        PixivHana.is_downloading = False
        self.progressbar.stop()

    def check_queue(self, iid=None):
        # 如果队列不为空,而且正在下载，就执行一次插入，然后200ms再检查队列
        if not PixivHana.queue.empty() and PixivHana.is_downloading:
            image = PixivHana.queue.get()
            self.insert_row(image, iid)
            self.update_idletasks()
            self.after(200, lambda: self.check_queue(iid))
            self.update_idletasks()
        # 如果下载已结束，队列不为空，就用while循环插入
        elif not PixivHana.is_downloading and not PixivHana.queue.empty():
            while not PixivHana.queue.empty():
                image = PixivHana.queue.get()
                self.insert_row(image, iid)
                self.update_idletasks()
            # 循环结束后，结束进度条
            self.progressbar.stop()
        # 如果还在下载，但是队列为空，那就过个500ms再来检查队列
        elif PixivHana.is_downloading and PixivHana.queue.empty():
            self.after(500, lambda: self.check_queue(iid))
        else:
            self.progressbar.stop()

    def insert_row(self, image, iid):
        try:
            iid = self.table_area.insert(
                parent='',
                index=END,
                values=(image["title"], image["user_name"], image["p_id"], image["status"])
            )
            self.table_area.selection_set(iid)  # 选择这一行，这样每次都选择最后一行
            self.table_area.see(iid)  # see方法用来滚动使所选的行可见
        except OSError:
            return


if __name__ == '__main__':
    root = ttk.Window("hana_pixiv", "cerculean")
    PixivHana(root)
    win_width = 750
    win_height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 2))
    root.geometry(f'{win_width}x{win_height}+{x}+{y}')
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(ico_code))
    tmp.close()
    root.iconbitmap("tmp.ico")
    os.remove("tmp.ico")
    root.mainloop()
