"""
show_num -  通过xml文字绘制数字

Author: hanayo
Date： 2024/1/19
"""

import matplotlib.pyplot as plt
import re

code_str = """
      <contour>
        <pt x="258" y="536" on="1"/>
        <pt x="106" y="592" on="0"/>
        <pt x="106" y="741" on="1"/>
        <pt x="106" y="853" on="0"/>
        <pt x="263" y="1000" on="0"/>
        <pt x="526" y="1000" on="0"/>
        <pt x="686" y="844" on="0"/>
        。。。此处省略一些代码

      </contour>
"""


x = [int(i) for i in re.findall(r'<pt x="(.*?)" y=', code_str)]
y = [int(i) for i in re.findall(r'y="(.*?)" on=', code_str)]

print(x)
print(y)

plt.plot(x, y)
plt.show()
