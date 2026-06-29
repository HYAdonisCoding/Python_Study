#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# 第6章 数据载入、存储及文件格式
from pathlib import Path

# import sys

# print(sys.path)
base_dir = Path(__file__).parent

# from src.DataAnalysis.Data_Wrangling.debug import p_info

from debug import p_info

# from utils.debug import p_info

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


# 6.1 文本格式数据的读写
def text_format_read_write():
    print(f"{speter*2}text_format_read_write{speter*2}")
    print(f"{speter*2}文本格式数据的读写{speter*2}")

    df = pd.read_csv(f"{base_dir}/examples/ex1.csv")
    df1 = pd.read_table(f"{base_dir}/examples/ex1.csv", sep=",")
    df3 = pd.read_csv(f"{base_dir}/examples/ex2.csv", header=None)
    df4 = pd.read_csv(
        f"{base_dir}/examples/ex2.csv", names=["a1", "b1", "c", "d", "message"]
    )

    names = ["a", "b", "c", "d", "message"]
    df5 = pd.read_csv(f"{base_dir}/examples/ex2.csv", names=names, index_col="message")

    p_info(df=df, df1=df1, df3=df3, df4=df4, df5=df5)
    parsed = pd.read_csv(
        f"{base_dir}/examples/csv_mindex.csv", index_col=["key1", "key2"]
    )
    result1 = list(open(f"{base_dir}/examples/ex3.txt"))
    # result2 = pd.read_table(f"{base_dir}/examples/ex3.txt", sep="\s+")

    ex4 = pd.read_csv(f"{base_dir}/examples/ex4.csv")
    ex4_ = pd.read_csv(f"{base_dir}/examples/ex4.csv", skiprows=[0, 2, 3])

    ex5 = pd.read_csv(f"{base_dir}/examples/ex5.csv")
    ex5_ = pd.read_csv(f"{base_dir}/examples/ex5.csv", na_values=["NULL"])

    sentinels = {"message": ["foo", "NA"], "something": ["two"]}
    ex5_1 = pd.read_csv(
        f"{base_dir}/examples/ex5.csv", na_values=sentinels, keep_default_na=False
    )
    p_info(
        parsed=parsed,
        result1=result1,
        result2=result2,
        ex4=ex4,
        ex4_=ex4_,
        ex5=ex5,
        ex5_n=pd.isnull(ex5),
        ex5_=ex5_,
        ex5_1=ex5_1,
    )


# 6.1.1 分块读入文本文件
def reading_text_files_in_chunks():
    print(f"{speter*2}reading_text_files_in_chunks{speter*2}")
    print(f"{speter*2}分块读入文本文件{speter*2}")

    pd.options.display.max_rows = 10
    result = pd.read_csv(f"{base_dir}/examples/ex6.csv")
    result1 = pd.read_csv(f"{base_dir}/examples/ex6.csv", nrows=5)
    chunker = pd.read_csv(f"{base_dir}/examples/ex6.csv", chunksize=1000)
    tot = pd.Series([], dtype="int64")
    for piece in chunker:
        tot = tot.add(piece["key"].value_counts(), fill_value=0)

    tot = tot.sort_values(ascending=False)
    p_info(
        result=result,
        result1=result1,
        chunker=chunker,
        chunker_t=type(chunker),
        tot=tot,
    )


import sys


# 6.1.2 将数据写入文本格式
def writing_data_to_text_format():
    print(f"{speter*2}writing_data_to_text_format{speter*2}")
    print(f"{speter*2}将数据写入文本格式{speter*2}")

    data = pd.read_csv(f"{base_dir}/examples/ex5.csv")
    data.to_csv(f"{base_dir}/examples/out.csv")
    data_out = pd.read_csv(f"{base_dir}/examples/out.csv")
    p_info(data=data, data_out=data_out)

    data_out1 = data.to_csv(sys.stdout, sep="|")
    p_info(data_out1=data_out1)
    data.to_csv(sys.stdout, na_rep="NULL")
    data.to_csv(sys.stdout, index=False, header=False)

    print()
    data.to_csv(sys.stdout, index=False, columns=["a", "b", "c"])

    print()
    dates = pd.date_range("1/1/2000", periods=7)
    ts = pd.Series(np.arange(7), index=dates)
    ts.to_csv(f"{base_dir}/examples/tseries.csv")
    p_info(
        series=Path(f"{base_dir}/examples/tseries.csv").read_text(),
        index_name=ts.index.name,
        series_name=ts.name,
    )


import csv


class my_dialect(csv.Dialect):
    lineterminator = "\n"
    delimiter = ";"
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL


# 6.1.3 使用分隔格式
def delimited_formats():
    print(f"{speter*2}delimited_formats{speter*2}")
    print(f"{speter*2}使用分隔格式{speter*2}")

    p_info(
        ex7=Path(f"{base_dir}/examples/ex7.csv").read_text(),
    )

    f = open(f"{base_dir}/examples/ex7.csv")
    reader = csv.reader(f)
    for line in reader:
        print(line)
    # f.close()

    with open(f"{base_dir}/examples/ex7.csv") as f:
        lines = list(csv.reader(f))
        header, values = lines[0], lines[1:]
        data_dict = {h: v for h, v in zip(header, zip(*values))}
        p_info(data_dict=data_dict)

        f.seek(0)
        reader = csv.reader(f, dialect=my_dialect)
        print("my_dialect:")

        for line in reader:
            print(line)

        f.seek(0)
        reader = csv.reader(f, delimiter="|")
        print("delimiter='|':")
        for line in reader:

            print(line)
    f.close()

    with open(f"{base_dir}/examples/out.csv", "a", newline="") as f:
        writer = csv.writer(f, dialect=my_dialect)
        writer.writerow(("one", "two", "three"))
        writer.writerow(("1", "2", "3"))
        writer.writerow(("4", "5", "6"))
        writer.writerow(("7", "8", "9"))
    p_info(read_text=Path(f"{base_dir}/examples/out.csv").read_text())


import json


# 6.1.4 JSON数据
def json_data():
    print(f"{speter*2}json_data{speter*2}")
    print(f"{speter*2}JSON数据{speter*2}")

    obj = """
    {"name": "Wes",
    "cities_lived": ["Akron", "Nashville", "New York", "San Francisco"],
    "pet": null,
    "siblings": [{"name": "Scott", "age": 34, "hobbies": ["guitars", "soccer"]},
                {"name": "Katie", "age": 42, "hobbies": ["diving", "art"]}]
    }
    """

    result = json.loads(obj)
    asjson = json.dumps(result)
    siblings = pd.DataFrame(result["siblings"], columns=["name", "age"])
    data = pd.read_json(f"{base_dir}/examples/example.json")

    p_info(
        title="json",
        result=result,
        asjson=asjson,
        siblings=siblings,
        data=data,
        to_json=data.to_json(),
        to_json1=data.to_json(orient="records"),
    )


from lxml import objectify
from io import StringIO


# 6.1.5 XML 和 HTML：网络抓取
def xml_html_web_scraping():
    print(f"{speter*2}xml_html_web_scraping{speter*2}")
    print(f"{speter*2}XML 和 HTML：网络抓取{speter*2}")

    tables = pd.read_html(f"{base_dir}/examples/fdic_failed_bank_list.html")
    failures = tables[0]
    close_timestamps = pd.to_datetime(failures["Closing Date"])

    p_info(
        len=len(tables),
        failures=failures.head(),
        value_counts=close_timestamps.dt.year.value_counts(),
    )

    # path = "datasets/mta_perf/Performance_MNR.xml"
    # with open(path) as f:
    #     parsed = objectify.parse(f)
    # root = parsed.getroot()

    # data = []

    # skip_fields = ["PARENT_SEQ", "INDICATOR_SEQ", "DESIRED_CHANGE", "DECIMAL_PLACES"]

    # for elt in root.INDICATOR:
    #     el_data = {}
    #     for child in elt.getchildren():
    #         if child.tag in skip_fields:
    #             continue
    #         el_data[child.tag] = child.pyval
    #     data.append(el_data)
    # perf = pd.DataFrame(data)
    # perf.head()

    tag = '<a href="https://www.google.com">Google</a>'
    root = objectify.parse(StringIO(tag)).getroot()
    p_info(root=root, href=root.get("href"), text=root.text)


# 6.2 二进制格式
def binary_formats():
    print(f"{speter*2}binary_formats{speter*2}")
    print(f"{speter*2}二进制格式{speter*2}")

    frame = pd.read_csv(f"{base_dir}/examples/ex1.csv")

    # frame.to_pickle(f"{base_dir}/examples/frame_pickle")

    frame1 = pd.read_pickle(f"{base_dir}/examples/frame_pickle")

    p_info(title="6.2", frame=frame, frame1=frame1)


# 6.2.1 使用 HDF5格式
def using_hdf5_format():
    print(f"{speter*2}using_hdf5_format{speter*2}")
    print(f"{speter*2}使用 HDF5格式{speter*2}")

    frame = pd.DataFrame({"a": np.random.randn(100)})
    store = pd.HDFStore(f"{base_dir}/examples/mydata.h5")
    store["obj1"] = frame
    store["obj1_col"] = frame["a"]
    p_info(title="HDFS", store=store, obj1=store["obj1"], obj1_col=store["obj1_col"])

    store.put("obj2", frame, format="table")
    p_info(obj2=store.select("obj2", where=["index >= 10 and index <=15"]))
    store.close()


# 6.2.2 读取 Microsoft Excel 文件
def reading_excel_files():
    print(f"{speter*2}reading_excel_files{speter*2}")
    print(f"{speter*2}读取 Microsoft Excel 文件{speter*2}")
    xlsx = pd.ExcelFile(f"{base_dir}/examples/ex1.xlsx")
    p_info(xlsx=pd.read_excel(xlsx, "Sheet1"))

    frame = pd.read_excel(f"{base_dir}/examples/ex1.xlsx", sheet_name="Sheet1")

    writer = pd.ExcelWriter(f"{base_dir}/examples/ex2.xlsx")

    frame.to_excel(writer, sheet_name="Sheet1")
    frame.to_excel(f"{base_dir}/examples/ex2.xlsx")
    p_info(
        frame=frame,
    )


import requests


# 6.3 与Web API 交互
def interacting_with_web_api():
    print(f"{speter*2}interacting_with_web_api{speter*2}")
    print(f"{speter*2}与Web API 交互{speter*2}")

    url = "https://api.github.com/repos/pandas-dev/pandas/issues"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    issues = pd.DataFrame(data, columns=["number", "title", "labels", "state"])
    p_info(resp=resp, t=data[0]["title"], issues=issues)


import sqlite3
import sqlalchemy as sqla


# 6.4 与数据库交互
def interacting_with_databases():
    print(f"{speter*2}interacting_with_databases{speter*2}")
    print(f"{speter*2}与数据库交互{speter*2}")

    query = """
    CREATE TABLE test
    (a VARCHAR(20), b VARCHAR(20),
    c REAL,        d INTEGER
    );"""

    con = sqlite3.connect(f"{base_dir}/mydata.sqlite")
    con.execute("DROP TABLE IF EXISTS test")
    con.execute(query)
    con.commit()
    data = [
        ("Atlanta", "Georgia", 1.25, 6),
        ("Tallahassee", "Florida", 2.6, 3),
        ("Sacramento", "California", 1.7, 5),
    ]
    stmt = "INSERT INTO test VALUES(?, ?, ?, ?)"

    con.executemany(stmt, data)
    con.commit()
    cursor = con.execute("SELECT * FROM test")
    rows = cursor.fetchall()
    p_info(
        rows=rows,
        d=cursor.description,
        df=pd.DataFrame(rows, columns=[x[0] for x in cursor.description]),
    )

    db = sqla.create_engine(f"sqlite:///{base_dir}/mydata.sqlite")
    data = pd.read_sql("SELECT * FROM test", db)
    p_info(data=data)


# 6.5 本章小结
def chapter_6_summary():
    print(f"{speter*2}chapter_6_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        interacting_with_databases()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
