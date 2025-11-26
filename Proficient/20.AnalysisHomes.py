#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 20 分析在售二手房数据 Analyzing data on existing homes for sale

# * 分析主页面
# 打开首页https://bj.lianjia.com/ershoufang/pg1/
# <li class="clear LOGCLICKDATA" data-lj_view_evtid="21625" data-lj_evtid="21624" data-lj_view_event="ItemExpo" data-lj_click_event="SearchClick" data-lj_action_source_type="链家_PC_二手列表页卡片" data-lj_action_click_position="0" data-lj_action_fb_expo_id="1045648294921654273" data-lj_action_fb_query_id="1045648294141513728" data-lj_action_resblock_id="1111027377528" data-lj_action_housedel_id="101133895297"><a class="noresultRecommend img LOGCLICKDATA" href="https://bj.lianjia.com/ershoufang/101133895297.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="101133895297" data-is_focus="" data-sl=""><!-- 热推标签、埋点 --><img src="https://s1.ljcdn.com/feroot/pc/asset/img/vr/vrlogo.png?_v=2025112415183059" class="vr_item"><img class="lj-lazy" src="https://image1.ljcdn.com/110000-inspection/pc1_oqXZjdJKI.jpg.296x216.jpg" data-original="https://image1.ljcdn.com/110000-inspection/pc1_oqXZjdJKI.jpg.296x216.jpg" alt="金隅丽港06年小区 人车分流 满五唯一、精致一居室" style="display: block;"></a><div class="info clear"><div class="title"><a class="" href="https://bj.lianjia.com/ershoufang/101133895297.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="101133895297" data-is_focus="" data-sl="">金隅丽港06年小区 人车分流 满五唯一、精致一居室</a><!-- 拆分标签 只留一个优先级最高的标签--><span class="goodhouse_tag tagBlock">必看好房</span></div><div class="flood"><div class="positionInfo"><span class="positionIcon"></span><a href="https://bj.lianjia.com/xiaoqu/1111027377528/" target="_blank" data-log_index="1" data-el="region">金隅丽港城 </a>   -  <a href="https://bj.lianjia.com/ershoufang/wangjing/" target="_blank">望京</a> </div></div><div class="address"><div class="houseInfo"><span class="houseIcon"></span>1室1厅 | 54.8平米 | 东 | 简装 | 低楼层(共26层) | 2004年 | 塔楼</div></div><div class="followInfo"><span class="starIcon"></span>11人关注 / 31天以前发布</div><div class="tag"><span class="subway">近地铁</span><span class="vr">VR房源</span><span class="five">房本满两年</span></div><div class="priceInfo"><div class="totalPrice totalPrice2"><i> </i><span class="">255</span><i>万</i></div><div class="unitPrice" data-hid="101133895297" data-rid="1111027377528" data-price="46533"><span>46,533元/平</span></div></div></div><div class="listButtonContainer"><div class="btn-follow followBtn" data-hid="101133895297"><span class="follow-text">关注</span></div><div class="compareBtn LOGCLICK" data-hid="101133895297" log-mod="101133895297" data-log_evtid="10230">加入对比</div></div></li>
# * 分析详情页
# 
# 筛选离地铁近的房源
def filter_listings_near_subway_stations():
    pass
# 分析各区域在售房源占比
def analyze_the_percentage_of_listings_for_sale_in_each_area():
    pass
# 分析在售房源的户型
def analyze_the_unit_types_of_listings_for_sale():
    pass
# 分析房龄和平米单价的关系
def analyze_the_relationship_between_building_age_and_price_per_square_meter():
    pass
# 分析在售房源小区的热度
def analyze_the_popularity_of_the_neighborhoods_where_listings_are_for_sale():
    pass
def test():
    pass
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        filter_listings_near_subway_stations()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
