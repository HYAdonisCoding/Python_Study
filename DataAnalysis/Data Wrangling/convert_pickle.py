#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# 第X章 。。。
from pathlib import Path

base_dir = Path(__file__).parent


def p_info(**kwargs):
    for name, value in kwargs.items():
        print(f"{name}:")
        print(value)
    print()


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

# pickle 转换需要使用旧版 pandas 环境
# Python 进程无法自动切换当前 shell 的虚拟环境，只能检测并提示


def check_old_environment():
    import sys
    import pandas as pd

    if pd.__version__ != "1.5.3":
        print("当前 pandas 版本:", pd.__version__)
        print("请使用 pandas_old 环境运行此脚本:")
        print("source pandas_old/bin/activate")
        print("python convert_pickle.py")
        sys.exit(1)


np.set_printoptions(linewidth=200)


def p_info(**kwargs):
    for name, value in kwargs.items():
        print(f"{name}: {value}")
    print("")


def test():
    print(f"{speter*2}test{speter*2}")
    path = f"{base_dir}/examples/segismundo.txt"


def convert_pickle(old_file, new_file):
    """

    使用旧 pandas 读取 pickle，

    保存为新版 pandas 可读取格式

    """

    print(f"{speter*2} Converting {old_file.name} {speter*2}")

    data = pd.read_pickle(old_file)

    p_info(shape=data.shape, columns=data.columns, head=data.head())

    data.to_pickle(new_file)

    print(f"Saved -> {new_file}")

    print()


def convert_all():

    examples_dir = base_dir / "examples"

    files = [
        "yahoo_price.pkl",
        "yahoo_volume.pkl",
    ]

    for file_name in files:

        old_file = examples_dir / file_name

        if not old_file.exists():

            print(f"Not found: {old_file}")

            continue

        new_file = examples_dir / file_name.replace(".pkl", "_new.pkl")

        convert_pickle(old_file, new_file)


if __name__ == "__main__":
    check_old_environment()
    print(f"{speter*2}Starting{speter*2}")
    try:
        convert_all()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:
        print(f"{speter*2}Finished{speter*2}")
