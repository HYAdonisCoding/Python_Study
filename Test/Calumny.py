from scipy.optimize import linprog
# 7X+2.8Y≤560
# 3X+9Y≤460
# 4X+4Y≤336，通过3个方程计算一下X、Y的值使500X+800Y最大
# 目标函数的系数
c = [-500, -800]  # 注意这里是最小化问题，所以目标函数系数需要取负值


# 不等式约束的系数矩阵
A = [
    [7, 2.8],
    [3, 9],
    [4, 4]
]

# 不等式约束右侧的值
b = [560, 460, 336]

# 定义变量的范围（可取任意非负值）
x_bounds = (0, None)
y_bounds = (0, None)

# 调用线性规划库求解
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# 输出结果
print("最大值:", -result.fun)  # 注意这里要取负值
print("X 的值:", result.x[0])
print("Y 的值:", result.x[1])


