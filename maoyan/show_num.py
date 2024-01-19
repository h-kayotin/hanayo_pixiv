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
        <pt x="686" y="738" on="1"/>
        <pt x="686" y="592" on="0"/>
        <pt x="538" y="536" on="1"/>
        <pt x="630" y="505" on="0"/>
        <pt x="727" y="372" on="0"/>
        <pt x="727" y="280" on="1"/>
        <pt x="727" y="150" on="0"/>
        <pt x="545" y="-24" on="0"/>
        <pt x="248" y="-24" on="0"/>
        <pt x="157" y="63" on="1"/>
        <pt x="67" y="147" on="0"/>
        <pt x="67" y="283" on="1"/>
        <pt x="67" y="381" on="0"/>
        <pt x="165" y="512" on="0"/>
      </contour>
      <contour>
        <pt x="232" y="745" on="1"/>
        <pt x="232" y="672" on="0"/>
        <pt x="325" y="584" on="0"/>
        <pt x="398" y="584" on="1"/>
        <pt x="465" y="584" on="0"/>
        <pt x="514" y="629" on="1"/>
        <pt x="560" y="672" on="0"/>
        <pt x="560" y="804" on="0"/>
        <pt x="466" y="897" on="0"/>
        <pt x="396" y="897" on="1"/>
        <pt x="323" y="897" on="0"/>
        <pt x="232" y="808" on="0"/>
      </contour>
      <contour>
        <pt x="193" y="283" on="1"/>
        <pt x="193" y="228" on="0"/>
        <pt x="241" y="132" on="0"/>
        <pt x="293" y="104" on="1"/>
        <pt x="340" y="77" on="0"/>
        <pt x="398" y="77" on="1"/>
        <pt x="442" y="77" on="0"/>
        <pt x="514" y="106" on="0"/>
        <pt x="543" y="134" on="1"/>
        <pt x="601" y="189" on="0"/>
        <pt x="601" y="368" on="0"/>
        <pt x="483" y="483" on="0"/>
        <pt x="393" y="483" on="1"/>
        <pt x="307" y="483" on="0"/>
        <pt x="193" y="370" on="0"/>
      </contour>
"""


x = [int(i) for i in re.findall(r'<pt x="(.*?)" y=', code_str)]
y = [int(i) for i in re.findall(r'y="(.*?)" on=', code_str)]

print(x)
print(y)

plt.plot(x, y)
plt.show()
