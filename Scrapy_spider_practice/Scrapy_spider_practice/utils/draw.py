import matplotlib.pyplot as plt

# 数据
x = [1, 2, 3, 4, 5]
y = [50, 70, 90, 60, 80]

# 创建图表
plt.figure(figsize=(8, 6))

# 绘制数据点
plt.plot(x, y, 'bo-', label='Trend Line')  # 'bo-' 表示蓝色圆点线条

# 添加标题和轴标签
plt.title('趋势图')
plt.xlabel('轮数')
plt.ylabel('缺陷数')

# 设置 x 和 y 轴的范围
plt.xlim(0, 6)
plt.ylim(0, 175)

# 设置 x 和 y 轴的刻度
plt.xticks([0, 1, 2, 3, 4, 5, 6])
plt.yticks([0, 70, 117, 89, 54, 158, 33])

# 显示图例
plt.legend(loc='upper left')

# 显示网格
plt.grid(True, which='major', linestyle='--', axis='y')

# 保存图表为图片文件
plt.savefig('trend_chart.png', bbox_inches='tight')

# 显示图表
plt.show()
