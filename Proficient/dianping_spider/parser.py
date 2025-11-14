#!/usr/bin/env python3
# coding: utf-8
from bs4 import BeautifulSoup
speter = "-" * 10
import os
import re
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_list_page(html: str) -> list[dict]:
    """
    解析大众点评列表页，提取店铺ID、店铺名称、推荐菜和店铺链接
    """
    soup = BeautifulSoup(html, "html.parser")
    shops = []

    # 关键改动：#shop-all-list li 而非 #shop-all-list > li
    for li in soup.select("#shop-all-list li"):
        # 1. 商家编号
        data_shopid = li.get("data-shopid")
        if not data_shopid:
            a_tag = li.select_one("a[data-shopid]")
            data_shopid = a_tag.get("data-shopid") if a_tag else None

        # 2. 商家名称
        h4_tag = li.select_one(".tit h4")
        shop_name = h4_tag.get_text(strip=True) if h4_tag else None

        # 3. 商家链接
        a_tag = li.select_one(".tit a[href]")
        shop_link = a_tag["href"] if a_tag else None

        # 4. 推荐菜
        recommend_tags = li.select(".recommend a.recommend-click")
        recommend_dishes = ", ".join(a.get_text(strip=True) for a in recommend_tags) if recommend_tags else ""

        # 5. 校验并加入结果
        if data_shopid and shop_name:
            shops.append({
                "data_shopid": data_shopid,
                "shop_name": shop_name,
                "recommend_dishes": recommend_dishes,
                "shop_link": shop_link
            })

    print(f"解析成功 {len(shops)} 家商户")
    return shops
def parse_detail_page(html: str) -> dict:
    """
    解析大众点评详情页，提取店铺详细信息和评论
    """
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # 1. 店铺ID data-shopid
    data_shopid = ""
    data_shopid = soup.select_one('[data-launch-shop-uuid]')
    if data_shopid and data_shopid.get("data-launch-shop-uuid"):
        data["data_shopid"] = data_shopid.get("data-launch-shop-uuid")

    # 2. 店铺名称 shop_name
    shop_name_tag = soup.select_one(".shop-name, h1.shop-name, h1")
    shop_name = shop_name_tag.get_text(strip=True) if shop_name_tag else ""
    data["shop_name"] = shop_name

    # 3. 评分 star_score: from star class or mid-rank-stars class
    star_score = ""
    star_tag = soup.select_one(".star, .mid-rank-stars")
    if star_tag:
        # Try to get float from class like mid-str45 (4.5)
        classes = star_tag.get("class", [])
        score_found = False
        for cls in classes:
            m = re.match(r"mid-str(\d+)", cls)
            if m:
                val = m.group(1)
                if len(val) == 2:
                    star_score = f"{val[0]}.{val[1]}"
                else:
                    star_score = val
                score_found = True
                break
        if not score_found:
            # fallback: get text and extract float
            text = star_tag.get_text(strip=True)
            m = re.search(r"(\d+(\.\d+)?)", text)
            if m:
                star_score = m.group(1)
    data["star_score"] = star_score

    # 4. 各项评分 score_text: from .comment-score .item, fallback to .middlePanel .scoreText.wx-text
    score_items = soup.select(".comment-score .item")
    score_texts = []
    for item in score_items:
        txt = item.get_text(strip=True)
        if txt:
            score_texts.append(txt)
    score_text_value = ", ".join(score_texts)
    if not score_text_value:
        # fallback: check for .middlePanel .scoreText.wx-text
        score_panel = soup.select_one(".middlePanel .scoreText.wx-text")
        if score_panel and score_panel.get_text(strip=True):
            score_text_value = score_panel.get_text(strip=True)
    data["score_text"] = score_text_value

    # 5. 人均 price: from .price or .average-price
    price_tag = soup.select_one(".price, .average-price")
    price = price_tag.get_text(strip=True) if price_tag else ""
    data["price"] = price

    # 6. 区域 region: from .shop-addr .region or similar
    region_tag = soup.select_one(".shop-addr .region, .region")
    region = region_tag.get_text(strip=True) if region_tag else ""
    data["region"] = region

    # 7. 分类 category: from .shop-addr .category or similar
    category_tag = soup.select_one(".shop-addr .category, .category")
    category = category_tag.get_text(strip=True) if category_tag else ""
    data["category"] = category

    # 8. 地址 desc_addr_txt: from .address or .shop-addr inner text
    address_tag = soup.select_one(".address")
    if address_tag and address_tag.get_text(strip=True):
        desc_addr_txt = address_tag.get_text(strip=True)
    else:
        shop_addr_tag = soup.select_one(".shop-addr")
        if shop_addr_tag:
            desc_addr_txt = shop_addr_tag.get_text(separator=" ", strip=True)
        else:
            desc_addr_txt = ""
    data["desc_addr_txt"] = desc_addr_txt

    # New extraction for physical address
    physical_address_tag = soup.select_one(".addressText.wx-text")
    if physical_address_tag and physical_address_tag.get_text(strip=True):
        data["address"] = physical_address_tag.get_text(strip=True)

    # 评分
    star_tag = soup.select_one("div.star-score.wx-view, div.star-score, .mid-rank-stars")
    if star_tag:
        data["star_score"] = star_tag.get_text(strip=True)

    # 评论总数
    reviews_tag = soup.select_one("span.reviews.wx-text, a.review-num b")
    if reviews_tag:
        m = re.search(r"(\d+)", reviews_tag.get_text(strip=True))
        data["reviews"] = int(m.group(1)) if m else 0
    else:
        data["reviews"] = 0

    # 地址
    addr_tag = soup.select_one("div.desc-addr.wx-view span.desc-addr-txt.wx-text, .shop-addr .addr")
    if addr_tag:
        data["desc_addr_txt"] = addr_tag.get_text(strip=True)

    # 人均、区域、分类等仍用你已有逻辑
    

    # 店铺名称（新版结构）
    shop_name_tag = soup.select_one(".shopName.wx-text")
    if shop_name_tag:
        data["shop_name"] = shop_name_tag.get_text(strip=True)

    # 营业时间
    biz_time_tag = soup.select_one(".biz-time.wx-text")
    if biz_time_tag:
        data["biz_time"] = biz_time_tag.get_text(strip=True)
    print(f"解析详情页字段数量: {len(data.keys())}")
    return data

if __name__ == "__main__":
    # 这里放置简单的测试代码，使用示例HTML字符串
    # with open(os.path.join(BASE_DIR, "page_list.html"), encoding="utf-8") as f:
    #     html = f.read()

    # soup = BeautifulSoup(html, "html.parser")

    # print("1️⃣ #shop-all-list 数量：", len(soup.select("#shop-all-list")))
    # print("2️⃣ li 数量：", len(soup.select("#shop-all-list li")))
    # print("3️⃣ 是否有 recommend-click:", len(soup.select("a.recommend-click")))
    # print("Parsing list page...")
    # list_data = parse_list_page(html)
    # print(list_data)

    with open(os.path.join(BASE_DIR, "page_Error.html"), encoding="utf-8") as f:
        example_detail_html = f.read()
    print("\nParsing detail page...")
    detail_data = parse_detail_page(example_detail_html)
    print(detail_data)
