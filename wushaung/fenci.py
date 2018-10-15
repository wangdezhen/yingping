

import jieba # 导入jieba模块，用于中文分词
import pandas as pd
import matplotlib.pyplot as plt # 导入matplotlib，用于生成2D图形

from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator# 导入wordcount，用于制作词云图

# 获取所有评论
df = pd.read_csv("comments.csv",names =["id","nickName","userLevel","cityName","content","score","startTime"])
comments = df["content"].tolist()


# 设置分词
comment_after_split = jieba.cut(str(comments), cut_all=False)  # 非全模式分词，cut_all=false
words = " ".join(comment_after_split)  # 以空格进行拼接
# # print(words)
#
# 设置屏蔽词
stopwords = STOPWORDS.copy()
stopwords.update({"电影","最后","就是","不过","这个","一个","感觉","这部","虽然","不是","真的","觉得","还是","但是"})


bg_image = plt.imread('bg.jpg')
#生成
wc=WordCloud(
    width=1024,
    height=768,
    background_color="white",
    max_words=200,
    mask=bg_image,            #设置图片的背景
    stopwords=stopwords,
    max_font_size=200,
    random_state=50,
    font_path='C:/Windows/Fonts/simkai.ttf'   #中文处理，用系统自带的字体
    ).generate(words)

#产生背景图片，基于彩色图像的颜色生成器
image_colors=ImageColorGenerator(bg_image)
#开始画图
plt.imshow(wc.recolor(color_func=image_colors))
#为背景图去掉坐标轴
plt.axis("off")
#保存云图
plt.show()
wc.to_file("评价.png")
