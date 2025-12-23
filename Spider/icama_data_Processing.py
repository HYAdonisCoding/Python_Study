#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import re
from collections import Counter

# ========= 参数 =========
input_file = "Processing/查重.xlsx"
output_file = "Processing/output.xlsx"
sheet_name = 0  # 或具体 sheet 名
col_a = "有效成分英文名"
col_b = "英文"
case_sensitive = False  # 是否区分大小写


# =======================
def test():
    # 1. 读取 Excel
    df = pd.read_excel(input_file, sheet_name=sheet_name)

    # 2. 文本预处理（统一小写 + 去空 + 处理 NaN）
    a_series = (
        df[col_a]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )
    b_series = (
        df[col_b]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # 3. 判断“包含关系”（列对列：A 列 对 全部 B 列）
    # 说明：
    # - A 列逐行取值
    # - B 列作为“词库”，只要命中任意一个即算匹配
    # - 采用完整单词匹配，避免 rid 命中 imidacloprid

    # 构建英文词库（去空、去重），并记录来源单元格
    # 结构：keyword_map = { "imidacloprid": ["B2", "B15"], ... }
    keyword_map = {}

    for idx, b in enumerate(b_series, start=2):  # start=2 对应 Excel 行号
        if not b:
            continue
        for k in re.split(r"[;,/]", b):
            k = k.strip()
            if not k:
                continue
            keyword_map.setdefault(k, []).append(f"B{idx}")

    match_list = []
    hit_word_list = []
    empty_row_count = 0

    for a in a_series:
        if not a:
            match_list.append(False)
            hit_word_list.append("")
            empty_row_count += 1
            continue

        hit_items = []
        for k, cells in keyword_map.items():
            pattern = rf"\b{re.escape(k)}\b"
            if re.search(pattern, a):
                for c in cells:
                    hit_items.append(f"{k}({c})")

        if hit_items:
            match_list.append(True)
            hit_word_list.append("; ".join(sorted(hit_items)))
        else:
            match_list.append(False)
            hit_word_list.append("")

    df["match"] = match_list
    df["命中英文"] = hit_word_list

    # 统计信息
    total_rows = len(df)
    hit_count = sum(match_list)

    print("==== 统计结果 ====")
    print(f"总行数: {total_rows}")
    print(f"命中数: {hit_count}")
    print(f"空行数: {empty_row_count}")
    print("=================")

    # 4. 写回 Excel
    df.drop(columns=["match"]).to_excel(output_file, index=False)

    # 5. 使用 openpyxl 高亮匹配单元格
    wb = load_workbook(output_file)
    ws = wb.active

    highlight = PatternFill(fill_type="solid", fgColor="FFF59D")  # 浅黄色

    for row_idx, is_match in enumerate(df["match"], start=2):
        if is_match:
            ws.cell(row=row_idx, column=1).fill = highlight  # 高亮 A 列

    wb.save(output_file)


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
