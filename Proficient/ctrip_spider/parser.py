#!/usr/bin/env python3
# coding: utf-8
from bs4 import BeautifulSoup
speter = "-" * 10
import os
import re
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_city_blocks(html):
    soup = BeautifulSoup(html, "html.parser")
    city_blocks = soup.select("div.city")

    results = []

    for city in city_blocks:
        item = {}

        # 基本属性
        item["travelId"] = city.get("data-travelid")

        # 标签
        tags = [span.get_text(strip=True) for span in city.select(".yj_type span")]
        item["tags"] = tags

        # 封面图
        img_tag = city.select_one(".city-image img")
        if img_tag:
            item["coverImage"] = img_tag.get("src")
            item["coverId"] = img_tag.get("data-travelcoverid")

        # 封面跳转链接
        link_tag = city.select_one(".city-image")
        if link_tag:
            item["coverLink"] = link_tag.get("href")

        # 城市
        city_name = city.select_one(".city-sub .city-name")
        item["cityName"] = city_name.get_text(strip=True) if city_name else None
        item["cityLink"] = city_name.get("href") if city_name else None

        # 标题 & 文章链接
        title_tag = city.select_one(".city-sub .cpt")
        if title_tag:
            item["title"] = title_tag.get("title")
            item["articleLink"] = title_tag.get("href")

        # 浏览 / 喜欢 / 回复
        item["views"] = city.select_one(".numview").get_text(strip=True) if city.select_one(".numview") else None
        item["likes"] = city.select_one(".want").get_text(strip=True) if city.select_one(".want") else None
        item["replies"] = city.select_one(".numreply").get_text(strip=True) if city.select_one(".numreply") else None

        # 作者信息
        author = city.select_one(".authorinfo a[target='_blank']:nth-of-type(2)")
        if author:
            item["authorName"] = author.get_text(strip=True)
            item["authorLink"] = author.get("href")

        author_avatar = city.select_one(".authorinfo img")
        if author_avatar:
            item["authorAvatar"] = author_avatar.get("src")

        time_tag = city.select_one(".authorinfo .time")
        item["publishDate"] = time_tag.get_text(strip=True) if time_tag else None

        results.append(item)

    return results


def parse_travel(html):
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # 1. like_id
    like_tag = soup.select_one("#TitleLike")
    if like_tag:
        result["like_id"] = like_tag.get("data-likeid")

    # 2. 基本信息（天数 / 时间 / 人均 / 和谁 / 玩法）
    info_block = soup.select_one(".ctd_content_controls")
    if info_block:
        text = info_block.get_text("\n", strip=True)

        patterns = {
            "days": r"天数[:：]\s*([\d]+)",
            "month": r"时间[:：]\s*([0-9一二三四五六七八九十]+)",
            "person_cost": r"人均[:：]\s*([\d]+)",
            "companions": r"和谁[:：]\s*([^\n]+)",
            "play": r"玩法[:：]\s*([^\n]+)",
        }

        for k, pat in patterns.items():
            m = re.search(pat, text)
            if m:
                result[k] = m.group(1).strip()

    # 3. 作者去了这些地方
    result["places"] = [
        a.get_text(strip=True)
        for a in soup.select(".author_poi .gs_a_poi")
    ]

    # 4. 发布时间
    pub = soup.select_one(".ctd_content > h3")
    if pub:
        result["publish_time"] = pub.get_text(strip=True).replace("发表于", "").strip()

    # 5. 正文内容（所有 p）
    paras = soup.select(".ctd_content p")
    content = []
    for p in paras:
        # 清除 img 等非文本标签
        for t in p.find_all(["img", "div"]):
            t.decompose()
        txt = p.get_text(" ", strip=True)
        if txt:
            content.append(txt)

    result["content"] = "\n".join(content)

    return result


def extract_basic_info(text):
    """
    从以下格式中解析字段：
    “天数：5 天 时间：12 月 人均：3000 元 和谁：和朋友 玩法：美食，摄影”
    """
    info = {}

    import re
    patterns = {
        "days": r"天数[:：]\s*([\d]+)\s*天",
        "month": r"时间[:：]\s*([0-9一二三四五六七八九十]+)\s*月",
        "person_cost": r"人均[:：]\s*([\d]+)\s*元",
        "companions": r"和谁[:：]\s*([^\s]+)",
        "play": r"玩法[:：]\s*([^\s]+)"
    }

    for k, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            info[k] = m.group(1)

    return info
if __name__ == "__main__":
    # 这里放置简单的测试代码，使用示例HTML字符串
    # with open(os.path.join(BASE_DIR, "TravelListHtml.html"), encoding="utf-8") as f:
    #     html = f.read()

    # soup = BeautifulSoup(html, "html.parser")

    # print("1️⃣ #shop-all-list 数量：", len(soup.select("#shop-all-list")))
    # print("2️⃣ li 数量：", len(soup.select("#shop-all-list li")))
    # print("3️⃣ 是否有 recommend-click:", len(soup.select("a.recommend-click")))
    # print("Parsing list page...")
    # list_data = parse_city_blocks(html)
    # print(list_data)

    with open(os.path.join(BASE_DIR, "travels.html"), encoding="utf-8") as f:
        example_detail_html = f.read()
    print("\nParsing detail page...")
    detail_data = parse_travel(example_detail_html)
    print(detail_data)
