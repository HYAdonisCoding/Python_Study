#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第13章 Python 建模库介绍
# ================================
from pathlib import Path

base_dir = Path(__file__).parent


from debug import p_info


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


def test():
    print(f"{speter*2}test{speter*2}")
    path = f"{base_dir}/examples/segismundo.txt"


# 13.1 pandas 与建模代码的结合
def pandas_and_modeling_code_integration():
    print(f"{speter*2}pandas_and_modeling_code_integration{speter*2}")
    print(f"{speter*2}pandas 与建模代码的结合{speter*2}")

    data = pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )
    p_info(
        data=data,
        c=data.columns,
        v=data.values,
    )

    df2 = pd.DataFrame(data.values, columns=["one", "two", "three"])
    df3 = data.copy()
    df3["strings"] = ["a", "b", "c", "d", "e"]
    model_cols = ["x0", "x1"]
    p_info(
        df2=df2,
        df3=df3,
        v=df3.values,
        v1=data.loc[:, model_cols].values,
    )

    data["category"] = pd.Categorical(["a", "b", "a", "a", "b"], categories=["a", "b"])

    p_info(
        data=data,
    )
    dummies = pd.get_dummies(data.category, prefix="category")
    data_with_dummies = data.drop("category", axis=1).join(dummies)
    p_info(
        data_with_dummies=data_with_dummies,
    )


import patsy


# 13.2 使用 Patsy 创建模型描述
def creating_model_descriptions_with_patsy():
    print(f"{speter*2}creating_model_descriptions_with_patsy{speter*2}")
    print(f"{speter*2}使用 Patsy 创建模型描述{speter*2}")

    data = pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )
    y, x = patsy.dmatrices("y ~ x0 + x1", data)
    p_info(
        data=data,
        y=y,
        x=x,
        ny=np.asanyarray(y),
        nx=np.asanyarray(x),
        dm=patsy.dmatrices("y ~ x0 + x1 + 0", data)[1],
    )

    coef, resid, _, _ = np.linalg.lstsq(x, y)
    p_info(coef=coef)
    coef = pd.Series(coef.squeeze(), index=x.design_info.column_names)
    p_info(coef1=coef)


# 13.2.1 Patsy 公式中的数据转换
def data_transformations_in_patsy_formulas():
    print(f"{speter*2}data_transformations_in_patsy_formulas{speter*2}")
    print(f"{speter*2}Patsy 公式中的数据转换{speter*2}")
    data = pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )
    y, X = patsy.dmatrices("y ~ x0 + np.log(np.abs(x1) + 1)", data)
    p_info(
        X=X,
    )
    y, X = patsy.dmatrices("y ~ standardize(x0) + center(x1)", data)
    p_info(
        X1=X,
    )
    new_data = pd.DataFrame(
        {"x0": [6, 7, 8, 9], "x1": [3.1, -0.5, 0, 2.3], "y": [1, 2, 3, 4]}
    )
    new_X = patsy.build_design_matrices([X.design_info], new_data)

    p_info(
        new_X=new_X,
    )
    y, X = patsy.dmatrices("y ~ I(x0 + x1)", data)
    p_info(
        X2=X,
    )


# 13.2.2 分类数据与 Patsy
def categorical_data_with_patsy():
    print(f"{speter*2}categorical_data_with_patsy{speter*2}")
    print(f"{speter*2}分类数据与 Patsy{speter*2}")
    data = pd.DataFrame(
        {
            "key1": ["a", "a", "b", "b", "a", "b", "a", "b"],
            "key2": [0, 1, 0, 1, 0, 1, 0, 0],
            "v1": [1, 2, 3, 4, 5, 6, 7, 8],
            "v2": [-1, 0, 2.5, -0.5, 4.0, -1.2, 0.2, -1.7],
        }
    )
    y, X = patsy.dmatrices("v2 ~ key1", data)
    p_info(
        X=X,
    )
    y, X1 = patsy.dmatrices("v2 ~ key1 + 0", data)

    y, X2 = patsy.dmatrices("v2 ~ C(key2)", data)
    p_info(
        X1=X1,
        X2=X2,
    )
    data["key2"] = data["key2"].map({0: "zero", 1: "one"})

    y, X3 = patsy.dmatrices("v2 ~ key1 + key2", data)
    X
    y, X4 = patsy.dmatrices("v2 ~ key1 + key2 + key1:key2", data)
    p_info(
        data=data,
        X3=X3,
        X4=X4,
    )


# 13.3 statsmodels 介绍
def statsmodels_introduction():
    print(f"{speter*2}statsmodels_introduction{speter*2}")
    print(f"{speter*2}statsmodels 介绍{speter*2}")


import statsmodels.api as sm
import statsmodels.formula.api as smf


def dnorm(mean, variance, size=1):
    rng = np.random.default_rng(seed=12345)
    if isinstance(size, int):
        size = (size,)
    return mean + np.sqrt(variance) * rng.standard_normal(*size)


# 13.3.1 评估线性模型
def evaluating_linear_models():
    print(f"{speter*2}evaluating_linear_models{speter*2}")
    print(f"{speter*2}评估线性模型{speter*2}")
    # To make the example reproducible
    rng = np.random.default_rng(seed=12345)

    N = 100
    X = np.c_[dnorm(0, 0.4, size=N), dnorm(0, 0.6, size=N), dnorm(0, 0.2, size=N)]
    eps = dnorm(0, 0.1, size=N)
    beta = [0.1, 0.3, 0.5]

    y = np.dot(X, beta) + eps
    p_info(
        x=X[:5],
        y=y[:5],
    )
    X_model = sm.add_constant(X)
    p_info(
        X_model=X_model[:5],
    )

    model = sm.OLS(y, X)
    results = model.fit()
    p_info(
        params=results.params,
        summary=results.summary(),
    )
    data = pd.DataFrame(X, columns=["col0", "col1", "col2"])
    data["y"] = y
    p_info(
        data=data[:5],
    )
    results = smf.ols("y ~ col0 + col1 + col2", data=data).fit()
    p_info(
        params=results.params,
        tvalues=results.tvalues,
        predict=results.predict(data[:5]),
    )


from statsmodels.tsa.ar_model import AutoReg


# 13.3.2 评估时间序列处理
def evaluating_time_series_processing():
    print(f"{speter*2}evaluating_time_series_processing{speter*2}")
    print(f"{speter*2}评估时间序列处理{speter*2}")
    init_x = 4

    values = [init_x, init_x]
    N = 1000

    b0 = 0.8
    b1 = -0.4
    noise = dnorm(0, 0.1, N)
    for i in range(N):
        new_x = values[-1] * b0 + values[-2] * b1 + noise[i]
        values.append(new_x)

    MAXLAGS = 5
    model = AutoReg(values, MAXLAGS)
    results = model.fit()
    p_info(
        params=results.params,
        summary=results.summary(),
    )


# 13.4 scikit-learn 介绍
def sklearn_introduction():
    print(f"{speter*2}sklearn_introduction{speter*2}")
    print(f"{speter*2}scikit-learn 介绍{speter*2}")

    train = pd.read_csv(f"{base_dir}/datasets/titanic/train.csv")
    test = pd.read_csv(f"{base_dir}/datasets/titanic/test.csv")
    p_info(
        train=train.head(4),
        train_isna_sum=train.isna().sum(),
        test_isna_sum=test.isna().sum(),
    )
    impute_value = train["Age"].median()
    train["Age"] = train["Age"].fillna(impute_value)
    test["Age"] = test["Age"].fillna(impute_value)
    train["IsFemale"] = (train["Sex"] == "female").astype(int)
    test["IsFemale"] = (test["Sex"] == "female").astype(int)
    predictors = ["Pclass", "IsFemale", "Age"]

    X_train = train[predictors].to_numpy()
    X_test = test[predictors].to_numpy()
    y_train = train["Survived"].to_numpy()
    p_info(
        X_train=X_train[:5],
        y_train=y_train[:5],
    )

    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    p_info(y_predict=y_predict[:10])
    from sklearn.linear_model import LogisticRegressionCV

    model_cv = LogisticRegressionCV(Cs=10)
    model_cv.fit(X_train, y_train)
    from sklearn.model_selection import cross_val_score

    model = LogisticRegression(C=10)
    scores = cross_val_score(model, X_train, y_train, cv=4)
    p_info(scores=scores)


# 13.5 继续你的教育
def continue_your_education():
    print(f"{speter*2}continue_your_education{speter*2}")
    print(f"{speter*2}继续你的教育{speter*2}")
   
    # 虽然我只带读者浏览了一些Pytion建機库的皮毛，但是有越来越多的框架用于各种统计和机器学习，可以用 Python 或用户界面来实现。
    # 本书特别关注数据规整，但还有许多其他书籍包含了关于建模和数据科学工具的内容。
    # 这些优秀的书籍包括：
    # • Introduction to Machine Learning with Python by Andreas Mueller and Sarah Guido (O' Reilly)
    # • Python Data Science Handbook by Jake VanderPlas (O' Reilly)
    # • Data Science from Scratch: First Principles with Python by Joel Grus (O' Reilly)
    # • Python Machine Learning by Sebastian Raschka (Packt Publishing)
    # • Hands-On Machine Learning with Scikit-Learn and TensorFlow by Aurélien Géron (O' Reilly)
    # 虽然书籍可以成宝贵的学习资源，但当底层开源软件发生变化时，它们有时会变得过时。熟悉各种统计或机器学习框架的文档以了解最新功能和API是个不错的主意。
     

if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        sklearn_introduction()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
