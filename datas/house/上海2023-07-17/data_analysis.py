"""
data_analysis - 基于房价数据简单做一些分析

Author: hanayo
Date： 2023/7/18
"""
import pandas as pd
from pandas import DataFrame


house_data = pd.read_excel(io="房价数据.xlsx", index_col="id")
# # 总体
# print("房子总价的平均值是：", f"{house_data['total'].mean():.2f}万元")
# print("单价的平均值是：", f"{house_data['unit'].mean():.2f}元")

# 最高的top10
print("总价最贵的top10是：\n", house_data.nlargest(10, "total"))
print("单价最贵的top10是：\n", house_data.nlargest(10, "unit"))

# # 最低的top10
print("总价最低的top10是：\n", house_data.nsmallest(10, "total"))
print("单价最低的top10是：\n", house_data.nsmallest(10, "unit"))
#
# # 分组统计,按照area来进行统计，看看各个区的情况
# area_df_total = house_data.groupby("area").total.mean()  # type: DataFrame
# print(area_df_total)
# print("各区的均价情况，按从高到低排序：", area_df_total.sort_values(by="", ascending=False))
