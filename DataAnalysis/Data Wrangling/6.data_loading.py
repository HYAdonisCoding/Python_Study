#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# 第6章 数据载入、存储及文件格式
from pathlib import Path
base_dir = Path(__file__).parent


# 6.1 文本格式数据的读写
def text_format_read_write():
    print(f"{speter*2}text_format_read_write{speter*2}")
    print(f"{speter*2}文本格式数据的读写{speter*2}")


# 6.1.1 分块读入文本文件
def reading_text_files_in_chunks():
    print(f"{speter*2}reading_text_files_in_chunks{speter*2}")
    print(f"{speter*2}分块读入文本文件{speter*2}")


# 6.1.2 将数据写入文本格式
def writing_data_to_text_format():
    print(f"{speter*2}writing_data_to_text_format{speter*2}")
    print(f"{speter*2}将数据写入文本格式{speter*2}")


# 6.1.3 使用分隔格式
def delimited_formats():
    print(f"{speter*2}delimited_formats{speter*2}")
    print(f"{speter*2}使用分隔格式{speter*2}")


# 6.1.4 JSON数据
def json_data():
    print(f"{speter*2}json_data{speter*2}")
    print(f"{speter*2}JSON数据{speter*2}")


# 6.1.5 XML 和 HTML：网络抓取
def xml_html_web_scraping():
    print(f"{speter*2}xml_html_web_scraping{speter*2}")
    print(f"{speter*2}XML 和 HTML：网络抓取{speter*2}")
    
# 6.1.5 XML 和 HTML：网络抓取
def xml_html_web_scraping():
    print(f"{speter*2}xml_html_web_scraping{speter*2}")
    print(f"{speter*2}XML 和 HTML：网络抓取{speter*2}")


# 6.2 二进制格式
def binary_formats():
    print(f"{speter*2}binary_formats{speter*2}")
    print(f"{speter*2}二进制格式{speter*2}")


# 6.2.1 使用 HDF5格式
def using_hdf5_format():
    print(f"{speter*2}using_hdf5_format{speter*2}")
    print(f"{speter*2}使用 HDF5格式{speter*2}")


# 6.2.2 读取 Microsoft Excel 文件
def reading_excel_files():
    print(f"{speter*2}reading_excel_files{speter*2}")
    print(f"{speter*2}读取 Microsoft Excel 文件{speter*2}")


# 6.3 与Web API 交互
def interacting_with_web_api():
    print(f"{speter*2}interacting_with_web_api{speter*2}")
    print(f"{speter*2}与Web API 交互{speter*2}")


# 6.4 与数据库交互
def interacting_with_databases():
    print(f"{speter*2}interacting_with_databases{speter*2}")
    print(f"{speter*2}与数据库交互{speter*2}")


# 6.5 本章小结
def chapter_6_summary():
    print(f"{speter*2}chapter_6_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")



if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        text_format_read_write()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


