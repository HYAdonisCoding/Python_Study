# -*- coding: utf-8 -*-

import re # 正则表达式，进行文字匹配

str = '''
<div class="item">
<div class="pic">
<em class="">1</em>
<a href="https://movie.douban.com/subject/1292052/">
<img alt="肖申克的救赎" class="" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg" width="100"/>
</a>
</div>
<div class="info">
<div class="hd">
<a class="" href="https://movie.douban.com/subject/1292052/">
<span class="title">肖申克的救赎</span>
<span class="title"> / The Shawshank Redemption</span>
<span class="other"> / 月黑高飞(港)  /  刺激1995(台)</span>
</a>
<span class="playable">[可播放]</span>
</div>
<div class="bd">
<p class="">
                            导演: 弗兰克·德拉邦特 Frank Darabont   主演: 蒂姆·罗宾斯 Tim Robbins /...<br/>
                            1994 / 美国 / 犯罪 剧情
                        </p>
<div class="star">
<span class="rating5-t"></span>
<span class="rating_num" property="v:average">9.7</span>
<span content="10.0" property="v:best"></span>
<span>2959128人评价</span>
</div>
<p class="quote">
<span class="inq">希望让人自由。</span>
</p>
</div>
</div>
</div>
'''
findImgSrc = re.compile(r'<img .*? src="(.*?)".*?/>', re.S)
def main():
    img = re.findall(findImgSrc, str)
    print(img)
    
    str1 = " hello     world "
    pattern = re.compile(r"\s+")
    str1 = re.sub(pattern, " ", str1)
    print(str1)  # "hello world"

if __name__ == '__main__':
    main()