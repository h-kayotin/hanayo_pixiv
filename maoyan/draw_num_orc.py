"""
draw_num_orc - 根据字符代码，绘制图形，用ocr库识别

Author: hanayo
Date： 2024/1/19
"""
from fontTools.ttLib import TTFont
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
import ddddocr


def read_num_by_draw(woff_font):
    # 将woff保存成ttf格式字体
    ttf_font = "font/font.ttf"
    img_size = 512
    font = TTFont(woff_font)
    font_img = ImageFont.truetype(ttf_font, img_size)
    ocr = ddddocr.DdddOcr(show_ad=False)
    font_dict = dict()
    for cmap_code, glyph_name in font.getBestCmap().items():

        # 实例化一个图片对象
        img = Image.new('1', (img_size, img_size), 255)

        # 绘制图片
        draw = ImageDraw.Draw(img)
        # 将编码读取成字节
        txt = chr(cmap_code)

        x, y = draw.textsize(txt, font=font_img)

        draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font_img, fill=0)
        bytes_io = BytesIO()
        img.save(bytes_io, format="PNG")
        # 识别字体
        word = ocr.classification(bytes_io.getvalue())
        # print(cmap_code, glyph_name, word)
        font_dict[glyph_name.replace('uni', '&#x').lower()] = word

    return font_dict


if __name__ == '__main__':
    res_dict = read_num_by_draw("font/e3dfe524.woff")
    print(res_dict)