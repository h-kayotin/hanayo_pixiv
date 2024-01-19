"""
comp_font - 通过基准字体，比较编码，找出新的字体字典

然后结果试验失败

Author: hanayo
Date： 2024/1/19
"""
import requests
from fontTools.ttLib import TTFont

font_dict = {
    'uniEB19': 9, 'uniE3EC': 2, 'uniF7D2': 4, 'uniED30': 1, 'uniF3E8': 5, 'uniF11C': 3,
    'uniEA60': 6, 'uniEF28': 8, 'uniEA6F': 0, 'uniE3DF': 7
}


def comp_font(font_name):
    if font_name == "e3dfe524.woff":
        print("本次字体和第一次一样")
        return font_dict

    font_url = f"//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/{font_name}"
    r = requests.get('http:'+font_url)
    with open(f"font/{font_name}", "wb") as code:
        code.write(r.content)
    print("字体不一致，下载新的字体")

    # 打开基准字体
    demo_font = TTFont("font/e3dfe524.woff")
    demo_list = demo_font.getGlyphNames()[1:-1]
    demo_uni_list = demo_font.getGlyphOrder()[2:]
    print(demo_list)
    print(demo_uni_list)

    # 打开新字体
    new_font = TTFont(f"font/{font_name}")
    new_font.saveXML(f"font/{font_name}.xml")
    # new_font = TTFont("font/20a70494.woff")
    new_list = new_font.getGlyphNames()[1:-1]
    new_uni_list = new_font.getGlyphOrder()[2:]

    new_dict = dict()
    for n_uni in new_uni_list:
        n_obj = new_font['glyf'][n_uni]
        for demo_uni in demo_uni_list:
            demo_obj = demo_font['glyf'][demo_uni]
            if n_obj == demo_obj:
                new_dict[n_uni] = font_dict[demo_uni]

    print(new_dict)
    return new_dict
