# -*- coding:utf-8 -*-

from wordcloud import WordCloud
import cv2
import jieba
import matplotlib.pyplot as plt

def show():
    """
    根据文章标题,制作中文词云
    :return: None
    """
    # 文本
    with open('36kr.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    cut_text = " ".join(jieba.cut(text))
    color_mask = cv2.imread('show.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path = "./FZSTK.TTF",
        # 设置背景色
        background_color = 'white',
        # 词云形状
        mask = color_mask,
        # 允许最大词汇
        max_words = 2000,
        # 最大号字体
        max_font_size = 40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('cloud.jpg')

    plt.imshow(wCloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    show()