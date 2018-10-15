import json
import pandas as pd

from pyecharts import Style # 导入Style类，用于定义样式风格
from pyecharts import Geo # 导入Geo组件，用于生成地理坐标类图


from pyecharts import Bar # 导入Geo组件，用于生成柱状图
df = pd.read_csv("comments.csv",names =["id","nickName","userLevel","cityName","content","score","startTime"])

# 处理地名数据，解决坐标文件中找不到地名的问题
def handle(cities):
    cities = cities.tolist()

    # 获取坐标文件中所有地名
    data = None
    with open(
            'C:/Users/Dedream/AppData/Local/Programs/Python/Python36/Lib/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)

        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break

        # 处理不存在的地名
        if count == len(data):

            while city in cities:
                cities.remove(city)

    # 写入覆盖坐标文件
    with open(
            'C:/Users/Dedream/AppData/Local/Programs/Python/Python36/Lib/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str

    return cities  # 把city返回



def render():


    city_counts = df.groupby("cityName").size()
    new_citys = handle(city_counts.index)

    tuple_city = list(city_counts.items())

    attr_values = []
    for item in tuple_city:
        #print(item[0],end=' ')
        if item[0] in new_citys:
            attr_values.append(item)


    # 定义样式
    style = Style(
        title_color='#fff',
        title_pos='center',
        width = 1200,
        height = 600,
        background_color='#404a59',
        subtitle_color='#fff'
    )
    #
    # 根据城市数据生成地理坐标图
    geo = Geo('《无双》评星人位置分布', '图表来源：CSDN博客-梦想橡皮擦', **style.init_style)
    attr, value = geo.cast(attr_values)

    geo.add('', attr, value, visual_range=[0, 2500],type="scatter",
            visual_text_color='#fff', symbol_size=10,
            is_visualmap=True, visual_split_number=10)
    geo.render('评星人位置分布-地理坐标图.html')

    # 根据城市数据生成柱状图

    city_sorted =  city_counts.sort_values(ascending=False).head(20)

    bar = Bar("《无双》评星人来源排行TOP20", "CSDN博客-梦想橡皮擦", **style.init_style)
    attr, value = bar.cast(list(city_sorted.items()))
    bar.add("", attr, value, is_visualmap=True, visual_range=[0, 2500], visual_text_color='#fff',label_color='#fff',xaxis_label_textcolor='#fff',yaxis_label_textcolor='#fff', is_more_utils=True,
            is_label_show=True)
    bar.render("评星人来源排行-柱状图.html")



if __name__ == '__main__':
    render()

## 生成饼图的操作 ####################################################################################
'''

from pyecharts import Pie # 导入Pie组件，用于生成饼图
import numpy
import pandas as pd

df = pd.read_csv("comments.csv",names =["id","nickName","userLevel","cityName","content","score","startTime"])

attr = ["一星", "二星", "三星", "四星", "五星"]
score = df.groupby("score").size()

value = [
    score.iloc[0] + score.iloc[1]+score.iloc[1],
    score.iloc[3] + score.iloc[4],
    score.iloc[5] + score.iloc[6],
    score.iloc[7] + score.iloc[8],
    score.iloc[9] + score.iloc[10],

]


pie = Pie('《无双》评星比例', title_pos='center', width=900)
pie.use_theme("dark")
pie.add("评分", attr, value, center=[60, 50],radius=[25, 75], rosetype='raea', is_legend_show=True, is_label_show=True )
pie.render('评星.html')
'''
## 生成饼图的操作 ####################################################################################
