#!/usr/bin/env python3
# coding: utf-8
import json
from bs4 import BeautifulSoup
speter = "-" * 10
import os
import re
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.select_one("ul.sellListContent[log-mod='list']")
    items = []

    if not ul:
        return items  # 没有列表，返回空

    for li in ul.select("li.clear.LOGVIEWDATA.LOGCLICKDATA"):
        item = {}
        # 房源详情页链接 & ID
        a_tag = li.select_one("a.noresultRecommend.img")
        if a_tag:
            item["house_id"] = a_tag.get("data-housecode")
            item["detail_url"] = a_tag.get("href")

        # 标题
        title_tag = li.select_one(".info .title a")
        item["title"] = title_tag.get_text(strip=True) if title_tag else None

        # 小区 & 区域
        community_tag = li.select_one(".flood .positionInfo a:nth-of-type(1)")
        region_tag = li.select_one(".flood .positionInfo a:nth-of-type(2)")
        item["community_name"] = community_tag.get_text(strip=True) if community_tag else None
        item["community_url"] = community_tag.get("href") if community_tag else None
        item["region"] = region_tag.get_text(strip=True) if region_tag else None
        item["region_url"] = region_tag.get("href") if region_tag else None

        # 房屋信息
        house_info = li.select_one(".address .houseInfo")
        if house_info:
            parts = [x.strip() for x in house_info.get_text().split("|")]
            item["bedrooms"] = parts[0] if len(parts) > 0 else None
            item["area"] = parts[1] if len(parts) > 1 else None
            item["orientation"] = parts[2] if len(parts) > 2 else None
            item["renovation"] = parts[3] if len(parts) > 3 else None
            item["floor"] = parts[4] if len(parts) > 4 else None
            item["year_built"] = parts[5] if len(parts) > 5 else None
            item["building_type"] = parts[6] if len(parts) > 6 else None

        # 关注人数 & 发布时间
        follow_tag = li.select_one(".followInfo")
        if follow_tag:
            text = follow_tag.get_text(strip=True)
            import re
            followers = re.search(r"(\d+)人关注", text)
            item["followers"] = int(followers.group(1)) if followers else None
            publish_time = re.search(r"(\d+[天月]以前发布)", text)
            item["publish_time"] = publish_time.group(1) if publish_time else None

        # 总价 & 单价
        total_price_tag = li.select_one(".priceInfo .totalPrice span")
        unit_price_tag = li.select_one(".priceInfo .unitPrice span")
        item["total_price"] = total_price_tag.get_text(strip=True) if total_price_tag else None
        item["unit_price"] = unit_price_tag.get_text(strip=True) if unit_price_tag else None

        items.append(item)

    return items


def parse_detail(html):
    soup = BeautifulSoup(html, "html.parser")
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    
    # 总价
    total_tag = soup.select_one("span.total")
    unit_tag = soup.select_one("span.unit span")
    if total_tag and unit_tag:
        data["total_price"] = f"{total_tag.get_text(strip=True)}{unit_tag.get_text(strip=True)}"

    # 单价
    unit_price_tag = soup.select_one(".unitPrice .unitPriceValue")
    if unit_price_tag:
        data["unit_price"] = unit_price_tag.get_text(strip=True)
        
    # === 房源编号 / 风险提示 ===
    house_code_tag = soup.select_one(".houseRecord .info")
    # risk_notice_tag = soup.select_one(".danger-notice")
    if house_code_tag:
        house_code = house_code_tag.get_text(strip=True)
        house_code = house_code.replace("举报", "")  # 去掉“举报”
        data['house_code'] = house_code
    else:
        data['house_code'] = None

    # data['risk_notice'] = risk_notice_tag.get_text(strip=True) if risk_notice_tag else None
    # === 基本属性 ===
    base_ul = soup.select_one(".introContent .base .content ul")
    if base_ul:
        for li in base_ul.select("li"):
            label_tag = li.select_one("span.label")
            if not label_tag:
                continue
            label = label_tag.get_text(strip=True)
            value = label_tag.next_sibling
            if value:
                value = value.strip()
            else:
                value = None

            # 映射字段名
            if label == "房屋户型":
                data["house_type"] = value
            elif label == "所在楼层":
                data["floor_info"] = value
            elif label == "建筑面积":
                data["build_area"] = value
            elif label == "户型结构":
                data["structure_type"] = value
            elif label == "套内面积":
                data["inner_area"] = value
            elif label == "建筑类型":
                data["building_type"] = value
            elif label == "房屋朝向":
                data["orientation"] = value
            elif label == "建筑结构":
                data["construction"] = value
            elif label == "装修情况":
                data["renovation"] = value
            elif label == "梯户比例":
                data["staircase_ratio"] = value
            elif label == "供暖方式":
                data["heating_type"] = value
            elif label == "配备电梯":
                data["has_elevator"] = value
            elif label == "楼层高度":
                data["floor_height"] = value

    # === 交易属性 ===
    trans_ul = soup.select_one(".introContent .transaction .content ul")
    if trans_ul:
        for li in trans_ul.select("li"):
            label_tag = li.select_one("span.label")
            value_tag = li.select("span")
            if not label_tag or len(value_tag) < 2:
                continue
            label = label_tag.get_text(strip=True)
            value = value_tag[1].get_text(strip=True)

            # 映射字段名
            if label == "挂牌时间":
                data["listing_date"] = value
            elif label == "交易权属":
                data["ownership_type"] = value
            elif label == "上次交易":
                data["last_transaction"] = value
            elif label == "房屋用途":
                data["usage"] = value
            elif label == "房屋年限":
                data["property_age"] = value
            elif label == "产权所属":
                data["property_right"] = value
            elif label == "抵押信息":
                data["mortgage_info"] = value
            elif label == "房本备件":
                data["documents_uploaded"] = value
    # 标签
    tags = [a.get_text(strip=True) for a in soup.select(".introContent .tags .content a.tag")]
    data["tags"] = tags

    # 核心卖点、小区介绍、周边配套、交通出行
    base_attributes = soup.select(".introContent .baseattribute")
    for attr in base_attributes:
        name_tag = attr.select_one(".name")
        content_tag = attr.select_one(".content")
        if not name_tag or not content_tag:
            continue
        key = name_tag.get_text(strip=True)
        value = content_tag.get_text(strip=True)
        if key == "核心卖点":
            data["core_selling_points"] = value
        elif key == "小区介绍":
            data["community_intro"] = value
        # elif key == "周边配套":
        #     data["surrounding_facilities"] = value
        # elif key == "交通出行":
        #     data["transportation"] = value
    return data


def extract_basic_info(text):
    """
    从以下格式中解析字段：
    “天数：5 天 时间：12 月 人均：3000 元 和谁：和朋友 玩法：美食，摄影”
    """
    info = {}

    

    return info
if __name__ == "__main__":
    # 这里放置简单的测试代码，使用示例HTML字符串
    with open(os.path.join(BASE_DIR, "list.html"), encoding="utf-8") as f:
        html = f.read()
    print("Parsing list page...")
    list_data = parse_list(html)
    print(list_data[0])
    # {'house_id': '101132458400', 'detail_url': 'https://bj.lianjia.com/ershoufang/101132458400.html', 'title': '融泽嘉园中路2号院  商品房满五唯一', 'community_name': '融泽嘉园中路2号院', 'community_url': 'https://bj.lianjia.com/xiaoqu/1120064286006600/', 'region': '回龙观', 'region_url': 'https://bj.lianjia.com/ershoufang/huilongguan2/', 'bedrooms': '2室1厅', 'area': '93.18平米', 'orientation': '南 北', 'renovation': '简装', 'floor': '高楼层(共27层)', 'year_built': '2013年', 'building_type': '板楼', 'followers': 18, 'publish_time': None, 'total_price': '399', 'unit_price': '42,821元/平'}

    with open(os.path.join(BASE_DIR, "details.html"), encoding="utf-8") as f:
        example_detail_html = f.read()
    print("\nParsing detail page...")
    detail_data = parse_detail(example_detail_html)
    print(detail_data)
