# -*- coding: utf-8 -*-
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3


def main():
    print('Hello, World!')
    con = sqlite3.connect('movietop250.db')
    cur = con.cursor()
    sql = 'select instrodction from movie_top250'
    data =cur.execute(sql)
    text = ""
    for item in data:
        text =text + item[0]
        #print(item[0])
    # print(text)
    cur.close()
    con.close()
    
    # 分词
    cut = jieba.cut(text)
    string = ' '.join(cut)
    # print(len(string), string)
    # img = Image.open('../static/img/tree.jpg')
    img = Image.open('./Flask_Douban/static/img/tree4.png')
    print(img)
    arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=arr,
        font_path='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    )
    wc.generate_from_text(string)
    
    # 绘制图片
    plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    
    # plt.show()
    plt.savefig('./Flask_Douban/static/img/word.png', dpi=800)

if __name__ == '__main__':
    main()