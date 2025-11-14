#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 18 分析电商网站销售数据 Analyzing sales data from e-commerce websites
# * 分析主页面
# 1.打开点评网北京首页
# https://www.dianping.com/beijing/ch10
# 2.检查html元素 数据实际存放位置 <div class="shop-list J_shop-list shop-all-list" id="shop-all-list">下的<ul>
# 3.每页有15条数据,一共50页数据
# 4.分别点击2、3、4页
# https://www.dianping.com/beijing/ch10/p2
# https://www.dianping.com/beijing/ch10/p3
# https://www.dianping.com/beijing/ch10/p4

# * 分享商家商品列表
# 1.商品名称
# <div class="tit">
#     <a onclick="LXAnalytics('moduleClick', 'shopname');document.hippo.ext({cl_i:1,query_id:'559167c7-2c2a-4021-978a-15108f960e2d'}).mv('cl_to_s','G9B5lBAWimhGRPnh');" data-click-name="shop_title_click" data-shopid="G9B5lBAWimhGRPnh" data-hippo-type="shop" title="北京宜宾招待所(南翠花街店)" target="_blank" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh">
#         <h4>北京宜宾招待所(南翠花街店)</h4>
#     </a>
#     <div class="promo-icon J_promo_icon">
#           <a rel="nofollow" data-click-name="shop_group_icon_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank" href="http://t.dianping.com/deal/1447305194" title="北京宜宾招待所!仅售95元！价值100元的代金券1张，可叠加使用。" class="igroup" data-hippo-dealgrp_type="" data-hippo-dealgrp_id="1447305194">
#           </a>
#     </div>
#   </div>
# 2.获取每个商品名称所在链接，href 为：https://www.dianping.com/shop/+data-shopid+#comment
# *列表页获取得的数据
# data-shopid 商家编号
# shopName 商家名称
# 推荐菜
# <div class="recommend">
# <span>推荐菜：</span>
# <a class="recommend-click" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh/dish190867664" data-click-name="shop_tag_dish_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank">红糖冰粉</a>
# <a class="recommend-click" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh/dish349582468" data-click-name="shop_tag_dish_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank">粉蒸肉</a>
# <a class="recommend-click" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh/dish397219048" data-click-name="shop_tag_dish_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank">宜宾燃抄手</a>
# </div>
# * 分析商品详情页
# data-shopid 商家编号
# shopName 商家名称
# star-score 商家评分
# scoreText 各项评分
# price 人均消费
# region 区域
# category 分类
# desc-addr-txt 地址
# reviews 总评论个数


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
