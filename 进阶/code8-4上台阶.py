# 10阶楼梯，每次上1个台阶或者上2个台阶，问一共有多少种走法？
# f(n) = f(n-1) + f(n-2)

def climb_stairs(n):
    if n <= 2:
        return n
    else:
        prev1, prev2 = 1, 2
        for _ in range(3, n+1):
            current = prev1 + prev2
            prev1, prev2 = prev2, current
        return prev2


import time

n = 30
# 记录开始时间
start_time = time.perf_counter()
print(f"走上 {n} 阶楼梯的方法数共有 {climb_stairs(n)} 种。")

# 记录结束时间
end_time = time.perf_counter()

# 计算执行时间
execution_time = end_time - start_time
print(f"动态规划方法执行时间: {execution_time:.8f} 秒")

def f(n):
    if n <=2 :
        return n
    else :
        return f(n-1) + f(n-2)
    
# 记录开始时间
start_time = time.perf_counter()
print(f"走上 {n} 阶楼梯的方法数共有 {f(n)} 种。")
# 记录结束时间
end_time = time.perf_counter()

# 计算执行时间
execution_time = end_time - start_time
print(f"递归方法执行时间: {execution_time:.8f} 秒")