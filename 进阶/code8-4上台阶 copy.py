import time

def climb_stairs(n):
    if n <= 2:
        return n
    prev1, prev2 = 1, 2
    for _ in range(3, n + 1):
        current = prev1 + prev2
        prev1, prev2 = prev2, current
    return prev2

def f(n):
    if n <= 2:
        return n
    return f(n - 1) + f(n - 2)

def measure_time(func, n, repetitions=10):
    times = []
    for _ in range(repetitions):
        start_time = time.perf_counter()
        result = func(n)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    avg_time = sum(times) / repetitions
    return result, avg_time

n = 30
repetitions = 10

# 测量动态规划方法
result_dp, avg_time_dp = measure_time(climb_stairs, n, repetitions)
print(f"走上 {n} 阶楼梯的方法数共有 {result_dp} 种。")
print(f"动态规划方法平均执行时间: {avg_time_dp:.8f} 秒")

# 测量递归方法
result_rec, avg_time_rec = measure_time(f, n, repetitions)
print(f"走上 {n} 阶楼梯的方法数共有 {result_rec} 种。")
print(f"递归方法平均执行时间: {avg_time_rec:.8f} 秒")

