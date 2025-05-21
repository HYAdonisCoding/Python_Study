import pandas as pd

def read_markdown_table(file_path):
    """读取 Markdown 表格，去除无效的分隔线，并转换为 DataFrame"""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 过滤掉空行，并去掉头尾空格
    lines = [line.strip() for line in lines if line.strip()]

    # 找到表头（第一行）和分隔线（第二行）
    header_line = lines[0]
    separator_line = lines[1] if len(lines) > 1 else ""

    # 解析列名
    headers = [col.strip() for col in header_line.split("|")[1:-1]]

    # 如果第二行是 "---"，跳过它
    data_lines = lines[2:] if "---" in separator_line else lines[1:]

    # 解析数据行
    data = []
    for line in data_lines:
        values = [val.strip() for val in line.split("|")[1:-1]]
        if len(values) == len(headers):  # 确保列数匹配
            data.append(values)

    # 转换为 DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df

def merge_table(file1, file2, output_file="merged_table.md"):
    """合并两个 Markdown 表格，去重并重新排序"""
    df1 = read_markdown_table(file1)
    df2 = read_markdown_table(file2)

    # 合并并去重
    df_combined = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)

    # 处理序号列（如果存在，则更新；否则新增）
    if "序号" in df_combined.columns:
        df_combined["序号"] = range(1, len(df_combined) + 1)
    else:
        df_combined.insert(0, "序号", range(1, len(df_combined) + 1))

    # 转换回 Markdown 并保存
    markdown_output = df_combined.to_markdown(index=False)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)

    print(f"合并完成，结果已保存为 {output_file}")



if __name__ == "__main__":
    # 合并 Markdown 表格
    merge_table('/Users/adam/Documents/Developer/MyGithub/Python_Study/Scrapy_spider_practice/Scrapy_spider_practice/Test/table1.md', '/Users/adam/Documents/Developer/MyGithub/Python_Study/Scrapy_spider_practice/Scrapy_spider_practice/Test/table2.md')