# 字典（dict）、集合（set）、列表（list）、元组（tuple）

# 返回元组（0号位置是所有奇数的和，1号位置是所有偶数的和）
# 计算1 + 3 + 5 + ... + n
# 计算2 + 4 + 6 + ... + n
def odd_even_sum(n):
    n += 1
    # 所有奇数的和
    o = [i for i in range(1, n , 2)]
    # 所有偶数的和
    e = [i for i in range(0, n , 2)]
    return sum(o), sum(e)


odd, even = odd_even_sum(10)

print(f'所有奇数的和是：{odd}, 所有偶数的和是：{even}')

# data = odd_even_sum(10)

# print(f'所有奇数的和是：{data[0]}, 所有偶数的和是：{data[1]}')


# 返回列表（0号位置是所有奇数的和，1号位置是所有偶数的和）
# 计算1 + 3 + 5 + ... + n
# 计算2 + 4 + 6 + ... + n
# def odd_even_sum(n):
#     n += 1
#     # 所有奇数的和
#     o = [i for i in range(1, n , 2)]
#     # 所有偶数的和
#     e = [i for i in range(0, n , 2)]
#     return [sum(o), sum(e)]


# data = odd_even_sum(10)

# print(f'所有奇数的和是：{data[0]}, 所有偶数的和是：{data[1]}')

# 返回集合
# 计算1 + 3 + 5 + ... + n
# 计算2 + 4 + 6 + ... + n
# def odd_even_sum(n):
#     n += 1
#     # 所有奇数的和
#     o = [i for i in range(1, n , 2)]
#     # 所有偶数的和
#     e = [i for i in range(0, n , 2)]
#     return {sum(o), sum(e)}


# data = odd_even_sum(10)

# print(f'结果是：{data}')

# 返回字典
# 计算1 + 3 + 5 + ... + n
# 计算2 + 4 + 6 + ... + n
# def odd_even_sum(n):
#     n += 1
#     # 所有奇数的和
#     o = [i for i in range(1, n , 2)]
#     # 所有偶数的和
#     e = [i for i in range(0, n , 2)]
#     return {
#         'o': sum(o),
#         'e': sum(e)
#         }


# data = odd_even_sum(10)

# print(f'所有奇数的和是：{data["o"]}, 所有偶数的和是：{data["e"]}')