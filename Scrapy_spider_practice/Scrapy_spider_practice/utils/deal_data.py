import pandas as pd

# 数据
data = {
    "月份": ["2024-12", "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06",
             "2024-07", "2024-08", "2024-09", "2024-10", "2024-11"],
    "工作天数": [16, 21, 17, 21, 21.5, 21, 18.5, 22, 20.5, 21, 19, 21],
    "工作时间(小时)": [161.9, 211.24, 180.22, 221.65, 215.07, 208.75, 181.21, 217.95, 187.51, 216.89, 205.06, 208.9],
    "加班小时数": [10.9, 1.65, 9.24, 8.9, 0, 0, 0, 1.25, 0, 16.83, 21.82, 11.5],
    "请假天数": [0, 1, 1.5, 0, 0.5, 0, 0.5, 1, 1.5, 0, 0, 0],
    "公出天数": [0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 添加计算列
df["加班天数"] = df["加班小时数"] / 8
df["剩余天数"] = df["工作天数"] + df["加班天数"] - df["请假天数"]

# 保存为Excel
output_path = "工作统计.xlsx"  # 保存路径
df.to_excel(output_path, index=False)
print(f"文件已成功保存为：{output_path}")