#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 19 分析旅游网站数据 Analyzing travel website data
# * 分析主页面
#  步骤 01 打开主页  https://you.ctrip.com/
# 推荐：https://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=14&Idea=0&Type=1&Plate=0
# 最新：https://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=2&Idea=0&Type=2&Plate=0
# 头条：https://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=2&Idea=0&Type=100&Plate=0

# <div class="city" data-travelid="3990253"><div class="yj_type"><span class="pic-tagico-5">头条</span><span class="pic-tagico-1">精华</span></div><a target="_blank" class="city-image" href="/travels/sanya61/3990253.html" rel="nofollow"><img data-travelcoverid="509095992" class="pic" width="228" height="152" src="https://dimg04.c-ctrip.com/images/0105y120008crbslg56DD_R_228_10000_Q90.jpg"></a><div class="city-sub"><a target="_blank" class="city-name" href="/place/sanya61.html">三亚</a>：<a target="_blank" class="cpt" title="海岛之冬，和闺蜜的三亚之旅" href="/travels/sanya61/3990253.html">海岛之冬，和闺蜜的三亚之旅</a><p class="opts"><i class="numview" title="浏览">16556</i> <i class="want" title="喜欢">96</i>&nbsp;&nbsp;<i class="numreply" title="回复">29</i></p></div><div class="authorinfo"><p class="author" data-authorid="14457689"><a class="imgnav" target="_blank" href="/members/639FFB8ED39F4BF7874FFA698BC7D725/journals" rel="nofollow"><img title="阿拖拖晓君" width="28" height="28" class="pic" src="https://dimg04.c-ctrip.com/images/0Z81r120008ehsou035F6_R_180_180.jpg"></a><a target="_blank" href="/members/639FFB8ED39F4BF7874FFA698BC7D725/journals" rel="nofollow" title="阿拖拖晓君">阿拖拖晓君</a>&nbsp;&nbsp;<i class="time">2020-12-30</i></p></div></div>


# ? 数据分析
# 分析“驴友”普遍去了哪些地方
# 分析“驴友”出现特点
# 推测“驴友”都喜欢在哪个季节出行
# 推测未来的热门景点
def test():
    pass


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
