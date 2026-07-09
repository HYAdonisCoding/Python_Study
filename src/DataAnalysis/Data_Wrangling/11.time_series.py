#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第11章 时间序列
# ================================

from pathlib import Path

base_dir = Path(__file__).parent


from debug import p_info


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)
from datetime import datetime


def test():
    print(f"{speter*2}test{speter*2}")
    path = f"{base_dir}/examples/segismundo.txt"


from datetime import timedelta


# 11.1 日期和时间数据的类型及工具
def datetime_types_and_tools():
    print(f"{speter*2}datetime_types_and_tools{speter*2}")
    print(f"{speter*2}日期和时间数据的类型及工具{speter*2}")
    now = datetime.now()
    delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)

    start = datetime(2011, 1, 7)

    p_info(
        now=now,
        year=now.year,
        month=now.month,
        day=now.day,
        delta=delta,
        delta_days=delta.days,
        delta_seconds=delta.seconds,
        start=start,
        start1=start + timedelta(12),
        start2=start - 2 * timedelta(12),
    )


from dateutil.parser import parse


# 11.1.1 字符串与 datetime 互相转换
def string_datetime_conversion():
    print(f"{speter*2}string_datetime_conversion{speter*2}")
    print(f"{speter*2}字符串与 datetime 互相转换{speter*2}")
    stamp = datetime(2011, 1, 3)
    value = "2011-01-03"

    datestrs = ["7/6/2011", "8/6/2011"]

    p_info(
        stamp=str(stamp),
        strftime=stamp.strftime("%Y-%m-%d"),
        value=datetime.strptime(value, "%Y-%m-%d"),
        datestrs=[datetime.strptime(x, "%m/%d/%Y") for x in datestrs],
        p1=parse("2011-01-03"),
        p2=parse("Jan 31, 1997 10:45 AM"),
        p3=parse("06/12/2011", dayfirst=True),
    )
    datestrs = ["2011-07-06 12:00:00", "2011-08-06 00:00:00"]
    idx = pd.to_datetime(datestrs + [None])

    p_info(
        datestrs=pd.to_datetime(datestrs),
        idx=idx,
        idx2=idx[2],
        isna=pd.isna(idx),
    )


# 11.2 时间序列基础
def time_series_basics():
    print(f"{speter*2}time_series_basics{speter*2}")
    print(f"{speter*2}时间序列基础{speter*2}")
    dates = [
        datetime(2011, 1, 2),
        datetime(2011, 1, 5),
        datetime(2011, 1, 7),
        datetime(2011, 1, 8),
        datetime(2011, 1, 10),
        datetime(2011, 1, 12),
    ]
    ts = pd.Series(np.random.standard_normal(6), index=dates)
    p_info(
        ts=ts,
        idx=ts.index,
        ts1=ts + ts[::2],
        idx_dtype=ts.index.dtype,
        idx_0=ts.index[0],
    )
    print(f"{speter*2}索引、选择、子集{speter*2}")
    stamp = ts.index[2]
    p_info(
        ts=ts[stamp],
        ts1=ts["1/10/2011"],
        ts2=ts["20110110"],
    )

    longer_ts = pd.Series(
        np.random.standard_normal(1000), index=pd.date_range("2000-01-01", periods=1000)
    )
    p_info(
        longer_ts=longer_ts,
        longer_ts1=longer_ts["2001"],
        longer_ts2=longer_ts["2001-05"],
        longer_ts3=ts[datetime(2011, 1, 7) :],
        ts=ts,
        ts1=ts["1/6/2011":"1/11/2011"],
        ts2=ts.truncate(after="1/9/2011"),
    )
    dates = pd.date_range("2000-01-01", periods=100, freq="W-WED")
    long_df = pd.DataFrame(
        np.random.standard_normal((100, 4)),
        index=dates,
        columns=["Colorado", "Texas", "New York", "Ohio"],
    )
    p_info(loc=long_df.loc["2001-05"])


# 11.2.1 索引、选择、子集
def time_series_indexing_selection_subset():
    print(f"{speter*2}time_series_indexing_selection_subset{speter*2}")


# 11.2.2 含有重复索引的时间序列
def time_series_with_duplicate_indexes():
    print(f"{speter*2}time_series_with_duplicate_indexes{speter*2}")
    print(f"{speter*2}含有重复索引的时间序列{speter*2}")

    dates = pd.DatetimeIndex(
        ["2000-01-01", "2000-01-02", "2000-01-02", "2000-01-02", "2000-01-03"]
    )
    dup_ts = pd.Series(np.arange(5), index=dates)
    grouped = dup_ts.groupby(level=0)

    p_info(
        dup_ts=dup_ts,
        is_unique=dup_ts.is_unique,
        dup_ts1=dup_ts["1/3/2000"],
        dup_ts2=dup_ts["1/2/2000"],
        mean=grouped.mean(),
        count=grouped.count(),
    )


# 11.3 日期范围、频率和移位
def date_ranges_frequencies_and_shifting():
    print(f"{speter*2}date_ranges_frequencies_and_shifting{speter*2}")
    print(f"{speter*2}日期范围、频率和移位{speter*2}")


# 11.3.1 生成日期范围
def generating_date_ranges():
    print(f"{speter*2}generating_date_ranges{speter*2}")
    print(f"{speter*2}生成日期范围{speter*2}")
    index = pd.date_range("2012-04-01", "2012-06-01")
    p_info(
        index=index,
        range=pd.date_range(start="2021-4-1", periods=20),
        range1=pd.date_range(end="2021-6-1", periods=20),
        range2=pd.date_range("2000-1-1", "2000-11-1", freq="BME"),
        range3=pd.date_range("2012-05-02 12:56:31", periods=5),
        range4=pd.date_range("2012-05-02 12:56:31", periods=5, normalize=True),
    )


from pandas.tseries.offsets import Hour, Minute


# 11.3.2 频率和日期偏置
def frequencies_and_date_offsets():
    print(f"{speter*2}frequencies_and_date_offsets{speter*2}")
    print(f"{speter*2}频率和日期偏置{speter*2}")

    hour = Hour()
    four_hours = Hour(4)
    monthly_dates = pd.date_range("2012-01-01", "2012-09-01", freq="WOM-3FRI")

    p_info(
        hour=hour,
        four_hours=four_hours,
        date_range=pd.date_range("2000-01-01", "2000-01-03 23:59", freq="4h"),
        add=Hour(2) + Minute(30),
        date_range1=pd.date_range("2000-01-01", periods=10, freq="1h30min"),
        list=list(monthly_dates),
    )


from pandas.tseries.offsets import Day, MonthEnd


# 11.3.3 移位（前向和后向）日期
def shifting_dates_forward_backward():
    print(f"{speter*2}shifting_dates_forward_backward{speter*2}")
    print(f"{speter*2}移位（前向和后向）日期{speter*2}")
    ts = pd.Series(
        np.random.standard_normal(4),
        index=pd.date_range("2000-01-01", periods=4, freq="ME"),
    )
    p_info(
        ts=ts,
        ts1=ts.shift(2),
        ts2=ts.shift(-2),
        ts3=ts.shift(2, freq="ME"),
        ts4=ts.shift(3, freq="D"),
        ts5=ts.shift(1, freq="90min"),
    )

    now = datetime(2011, 11, 17)

    offset = MonthEnd()

    p_info(
        now=now + 3 * Day(),
        now1=now + MonthEnd(),
        now2=now + MonthEnd(2),
        o1=offset.rollforward(now),
        o2=offset.rollback(now),
    )

    ts = pd.Series(
        np.random.standard_normal(20),
        index=pd.date_range("2000-01-15", periods=20, freq="4D"),
    )

    p_info(
        ts=ts,
        mean=ts.groupby(MonthEnd().rollforward).mean(),
        m1=ts.resample("ME").mean(),
    )


import pytz


# 11.4 时区处理
def timezone_handling():
    print(f"{speter*2}timezone_handling{speter*2}")
    print(f"{speter*2}时区处理{speter*2}")

    tz = pytz.timezone("America/New_York")
    tz1 = pytz.timezone("Asia/Shanghai")
    dt = datetime.now(tz1)
    p_info(
        p=pytz.common_timezones[-5:],
        tz=tz,
        tz1=tz1,
        dt=dt,
    )


# 11.4.1 时区的本地化和转换
def timezone_localization_and_conversion():
    print(f"{speter*2}timezone_localization_and_conversion{speter*2}")
    print(f"{speter*2}时区的本地化和转换{speter*2}")

    dates = pd.date_range("2012-03-09 09:30", periods=6)
    ts = pd.Series(np.random.standard_normal(len(dates)), index=dates)
    ts_utc = ts.tz_localize("UTC")
    ts_eastern = ts.tz_localize("America/New_York")

    p_info(
        dates=dates,
        ts=ts,
        tz=ts.index.tz,
        d=pd.date_range("2012-03-09 09:30", periods=10, tz="UTC"),
        ts_utc=ts_utc,
        idx=ts_utc.index,
        us=ts_utc.tz_convert("America/New_York"),
        utc=ts_eastern.tz_convert("UTC"),
        eur=ts_eastern.tz_convert("Europe/Berlin"),
        sh=ts.index.tz_localize("Asia/Shanghai"),
    )


# 11.4.2 时区感知时间戳对象的操作
def timezone_aware_timestamp_operations():
    print(f"{speter*2}timezone_aware_timestamp_operations{speter*2}")
    print(f"{speter*2}时区感知时间戳对象的操作{speter*2}")

    stamp = pd.Timestamp("2011-03-12 04:00")
    stamp_utc = stamp.tz_localize("utc")

    stamp_moscow = pd.Timestamp("2011-03-12 04:00", tz="Europe/Moscow")

    p_info(
        stamp=stamp,
        stamp_utc=stamp_utc,
        New_York=stamp_utc.tz_convert("America/New_York"),
        stamp_moscow=stamp_moscow,
        New_York1=stamp_utc.tz_convert("America/New_York").value,
    )
    stamp = pd.Timestamp("2012-03-11 01:30", tz="US/Eastern")
    p_info(
        stamp=stamp,
        stamp1=stamp + Hour(),
    )
    stamp = pd.Timestamp("2012-11-04 00:30", tz="US/Eastern")
    p_info(
        stamp=stamp,
        stamp1=stamp + 2 * Hour(),
    )


# 11.4.3 不同时区间的操作
def operations_between_timezones():
    print(f"{speter*2}operations_between_timezones{speter*2}")
    print(f"{speter*2}不同时区间的操作{speter*2}")
    dates = pd.date_range("2012-03-07 09:30", periods=10, freq="B")
    ts = pd.Series(np.random.standard_normal(len(dates)), index=dates)
    ts1 = ts[:7].tz_localize("Europe/London")
    ts2 = ts1[2:].tz_convert("Europe/Moscow")
    result = ts1 + ts2
    p_info(
        ts=ts,
        ts1=ts1,
        ts2=ts2,
        idx=result.index,
    )


# 11.5 时间区间和区间算术
def time_periods_and_period_arithmetic():
    print(f"{speter*2}time_periods_and_period_arithmetic{speter*2}")
    print(f"{speter*2}时间区间和区间算术{speter*2}")

    p = pd.Period("2007", freq="Y-DEC")
    p_info(
        p=p,
        p_5=p + 5,
        p_2=p - 2,
        p1=pd.Period("2014", freq="Y-DEC") - p,
    )
    periods = pd.period_range("2000-01-01", "2000-06-30", freq="M")

    values = ["2001Q3", "2002Q2", "2003Q1"]
    index = pd.PeriodIndex(values, freq="Q-DEC")

    p_info(
        periods=periods,
        r=pd.Series(np.random.standard_normal(6), index=periods),
        index=index,
    )


# 11.5.1 区间频率转换
def period_frequency_conversion():
    print(f"{speter*2}period_frequency_conversion{speter*2}")
    print(f"{speter*2}区间频率转换{speter*2}")
    p = pd.Period("2011", freq="Y-DEC")
    p_info(
        p=p,
        ps=p.asfreq("M", how="start"),
        pe=p.asfreq("M", how="end"),
        pm=p.asfreq("M"),
    )
    p = pd.Period("2011", freq="Y-JUN")
    p_info(
        title="JUN",
        p=p,
        ps=p.asfreq("M", how="start"),
        pe=p.asfreq("M", how="end"),
        pm=p.asfreq("M"),
    )
    p = pd.Period("Aug-2011", "M")
    p_info(
        title="Aug",
        p=p,
        pa=p.asfreq("Y-JUN"),
    )
    periods = pd.period_range("2006", "2009", freq="Y-DEC")
    ts = pd.Series(np.random.standard_normal(len(periods)), index=periods)
    p_info(
        title="Y-DEC",
        ts=ts,
        ts_s=ts.asfreq("M", how="start"),
        ts_b=ts.asfreq("B", how="end"),
    )


# 11.5.2 季度区间频率
def quarterly_period_frequency():
    print(f"{speter*2}quarterly_period_frequency{speter*2}")
    print(f"{speter*2}季度区间频率{speter*2}")
    p = pd.Period("2012Q4", freq="Q-JAN")
    p_info(
        title="Q-JAN", p=p, ps=p.asfreq("D", how="start"), pe=p.asfreq("D", how="end")
    )
    p4pm = (p.asfreq("B", how="end") - 1).asfreq("min", how="start") + 16 * 60
    p_info(
        title="季度",
        p4pm=p4pm,
        pt=p4pm.to_timestamp(),
    )
    periods = pd.period_range("2011Q3", "2012Q4", freq="Q-JAN")
    ts = pd.Series(np.arange(len(periods)), index=periods)
    p_info(title="Q-JAN", ts=ts)
    new_periods = (periods.asfreq("B", "end") - 1).asfreq("h", "start") + 16
    ts.index = new_periods.to_timestamp()
    p_info(title="new_periods", ts=ts)


# 11.5.3 将时间戳转换区间（以及逆转换）
def timestamp_period_conversion():
    print(f"{speter*2}timestamp_period_conversion{speter*2}")
    print(f"{speter*2}将时间戳转换区间（以及逆转换）{speter*2}")
    dates = pd.date_range("2000-01-01", periods=3, freq="ME")
    ts = pd.Series(np.random.standard_normal(3), index=dates)

    pts = ts.to_period()

    dates = pd.date_range("2000-01-29", periods=6)
    ts2 = pd.Series(np.random.standard_normal(6), index=dates)

    p_info(
        title="timestamp_period_conversion",
        ts=ts,
        pts=pts,
        ts2=ts2,
        ts2_=ts2.to_period("M"),
    )
    pts = ts2.to_period()
    p_info(
        title="to_period",
        pts=pts,
        end=pts.to_timestamp(how="end"),
    )


# 11.5.4 从数组生成 PeriodIndex
def creating_periodindex_from_arrays():
    print(f"{speter*2}creating_periodindex_from_arrays{speter*2}")
    print(f"{speter*2}从数组生成 PeriodIndex{speter*2}")
    data = pd.read_csv(f"{base_dir}/examples/macrodata.csv")
    p_info(
        title="macrodata",
        data=data.head(5),
    )
    # index = pd.PeriodIndex(year=data["year"], quarter=data["quarter"], freq="Q-DEC")
    index = pd.PeriodIndex(
        data["year"].astype(str) + "Q" + data["quarter"].astype(str), freq="Q-DEC"
    )
    data.index = index
    p_info(
        title="macrodata",
        year=data["year"],
        quarter=data["quarter"],
        index=index,
        inf1=data["infl"],
        datanew=data.head(5),
    )


# 11.6 重新采样与频率转换
def resampling_and_frequency_conversion():
    print(f"{speter*2}resampling_and_frequency_conversion{speter*2}")
    print(f"{speter*2}重新采样与频率转换{speter*2}")

    dates = pd.date_range("2000-01-01", periods=100)

    ts = pd.Series(np.random.standard_normal(len(dates)), index=dates)

    p_info(
        title="重新采样与频率转换1",
        ts=ts,
        mean=ts.resample("ME").mean(),
        p=ts.resample("ME").mean().to_period(),
    )


# 11.6.1 向下采样
def downsampling():
    print(f"{speter*2}downsampling{speter*2}")
    print(f"{speter*2}向下采样{speter*2}")
    dates = pd.date_range("2000-01-01", periods=12, freq="min")
    ts = pd.Series(np.arange(len(dates)), index=dates)
    p_info(
        title="向下采样1",
        ts=ts,
        ts1=ts.resample("5min").sum(),
        ts2=ts.resample("5min", closed="right").sum(),
        ts3=ts.resample("5min", closed="right", label="right").sum(),
        ts4=ts.resample("5min", closed="right", label="right", offset="-1s").sum(),
    )
    p_info(
        title="向下采样2",
        ts=ts.resample("5min").ohlc(),
    )


# 11.6.2 向上采样与插值
def upsampling_and_interpolation():
    print(f"{speter*2}upsampling_and_interpolation{speter*2}")
    print(f"{speter*2}向上采样与插值{speter*2}")
    frame = pd.DataFrame(
        np.random.standard_normal((2, 4)),
        index=pd.date_range("2000-01-01", periods=2, freq="W-WED"),
        columns=["Colorado", "Texas", "New York", "Ohio"],
    )
    df_daily = frame.resample("D").asfreq()
    p_info(
        title="向上采样与插值1",
        frame=frame,
        df_daily=df_daily,
        d=frame.resample("D").ffill(),
        d1=frame.resample("D").ffill(limit=2),
        d2=frame.resample("W-THU").ffill(),
    )


# 11.6.3 使用区间进行重新采样
def resampling_with_periods():
    print(f"{speter*2}resampling_with_periods{speter*2}")
    print(f"{speter*2}使用区间进行重新采样{speter*2}")

    frame = pd.DataFrame(
        np.random.standard_normal((24, 4)),
        index=pd.period_range("1-2000", "12-2001", freq="M"),
        columns=["Colorado", "Texas", "New York", "Ohio"],
    )
    annual_frame = frame.resample("Y-DEC").mean()
    p_info(
        title="使用区间进行重新采样1",
        frame=frame,
        annual_frame=annual_frame,
        # Q-DEC: Quarterly, year ending in December
        a1=annual_frame.resample("Q-DEC").ffill(),
        a2=annual_frame.resample("Q-DEC", convention="end").asfreq(),
        a3=annual_frame.resample("Q-MAR").ffill(),
    )


# 11.7 移动窗口函数
def moving_window_functions():
    print(f"{speter*2}moving_window_functions{speter*2}")
    print(f"{speter*2}移动窗口函数{speter*2}")
    close_px_all = pd.read_csv(
        f"{base_dir}/examples/stock_px.csv", parse_dates=True, index_col=0
    )
    close_px = close_px_all[["AAPL", "MSFT", "XOM"]]
    close_px = close_px.resample("B").ffill()
    p_info(
        title="移动窗口函数1",
        AAPL=close_px["AAPL"].plot(),
        AAPL_m=close_px["AAPL"].rolling(250).mean().plot(),
    )
    plt.figure()
    std250 = close_px["AAPL"].pct_change().rolling(250, min_periods=10).std()
    p_info(
        title="移动窗口函数2",
        s50=std250[5:12],
    )
    std250.plot()

    expanding_mean = std250.expanding().mean()

    plt.style.use("grayscale")
    close_px.rolling(60).mean().plot(logy=True)

    p_info(
        title="移动窗口函数2",
        mean=close_px.rolling("20D").mean(),
    )

    show_plot()


def show_plot(seconds=8, save_path=None, title=None, dpi=400):
    if title:

        plt.title(title)
    if save_path:
        plt.savefig(f"{base_dir}/{save_path}", dpi=dpi, bbox_inches="tight")
        p_info(title="save successed", save_path=f"{base_dir}/{save_path}")

    plt.show(block=False)
    plt.pause(seconds)
    plt.close()


# 11.7.1 指数加权函数
def exponentially_weighted_functions():
    print(f"{speter*2}exponentially_weighted_functions{speter*2}")
    print(f"{speter*2}指数加权函数{speter*2}")
    close_px_all = pd.read_csv(
        f"{base_dir}/examples/stock_px.csv", parse_dates=True, index_col=0
    )
    close_px = close_px_all[["AAPL", "MSFT", "XOM"]]
    aapl_px = close_px["AAPL"]["2006":"2007"]

    ma30 = aapl_px.rolling(30, min_periods=20).mean()
    ewma30 = aapl_px.ewm(span=30).mean()

    aapl_px.plot(style="k-", label="Price")
    ma30.plot(style="k--", label="Simple Moving Avg")
    ewma30.plot(style="k-", label="EW MA")
    plt.legend()
    show_plot()


from scipy.stats import percentileofscore


# 11.7.2 二元移动窗口函数
def binary_moving_window_functions():
    print(f"{speter*2}binary_moving_window_functions{speter*2}")
    print(f"{speter*2}二元移动窗口函数{speter*2}")
    close_px_all = pd.read_csv(
        f"{base_dir}/examples/stock_px.csv", parse_dates=True, index_col=0
    )
    close_px = close_px_all[["AAPL", "MSFT", "XOM"]]
    spx_px = close_px_all["SPX"]
    spx_rets = spx_px.pct_change()
    returns = close_px.pct_change()
    corr = returns["AAPL"].rolling(125, min_periods=100).corr(spx_rets)
    corr.plot()

    corr = returns.rolling(125, min_periods=100).corr(spx_rets)
    corr.plot()

    # show_plot()
    plt.figure()
    # 11.7.3 用户自定义的移动窗口函数
    # def custom_moving_window_functions():
    print(f"{speter*2}custom_moving_window_functions{speter*2}")
    print(f"{speter*2}用户自定义的移动窗口函数{speter*2}")

    def score_at_2percent(x):
        return percentileofscore(x, 0.02)

    result = returns["AAPL"].rolling(250).apply(score_at_2percent)
    result.plot()
    show_plot()


# 11.8 本章小结
def chapter_11_summary():
    print(f"{speter*2}chapter_11_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")
    show_plot()


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        binary_moving_window_functions()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
