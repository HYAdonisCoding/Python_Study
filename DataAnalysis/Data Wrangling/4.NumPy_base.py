#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# 第4章 NumPy 基础
from pathlib import Path
base_dir = Path(__file__).parent
def p_info(**kwargs):
    for name, value in kwargs.items():
        print(f'{name}: \n{value}')
    print("")
def test():
    print(f"{speter*2}test{speter*2}")
    path = f'{base_dir}/examples/segismundo.txt'
import numpy as np
import matplotlib.pyplot as plt
import time

def test():
    my_arr = np.arange(10_000_000)
    my_list = list(range(10_000_000))
    # 测试 NumPy
    start = time.time()
    my_arr2 = my_arr * 2
    end = time.time()
    print(f"NumPy array 运算耗时: {end-start:.6f} 秒")
    # 测试 Python List
    start = time.time()
    my_list2 = [x * 2 for x in my_list]
    end = time.time()
    print(f"Python list 运算耗时: {end-start:.6f} 秒")
    
# NumPy ndarray：多维数组对象  
def numpy_ndarray_multi_dimensional_array_object():
    print(f"{speter*2}numpy_ndarray_multi_dimensional_array_object{speter*2}")
    print(f"{speter*2}NumPy ndarray：多维数组对象{speter*2}")
    
    
    # 生成随机数组
    data = np.random.randn(2, 3)
    print("生成随机数组", data)
    print("数学操作1", data*10)
    print("数学操作2", data+data)
    print(data.shape)
    print(data.dtype)
    
    # np.random.seed(12345)
    
    # plt.rc("figure", figsize=(10, 6))
    # np.set_printoptions(precision=4, suppress=True)

# 生成 ndarray  
def generate_ndarray():
    print(f"{speter*2}generate_ndarray{speter*2}")
    data1 = [6, 7.5, 8, 0, 1]
    arr1 = np.array(data1)
    print('arr1', arr1)
    data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
    arr2 = np.array(data2)
    print('arr2', arr2)
    print('ndim', arr2.ndim)
    print('shape', arr2.shape)
    print('arr1.dtype', arr1.dtype)
    print('arr2.dtype', arr2.dtype)
    
    zarray = np.zeros(10)
    p_info(zarray=zarray)
    zarray1 = np.zeros((3, 6))
    p_info(zarray1=zarray1)
    
    arange1 = np.arange(15)
    p_info(arange1=arange1)
    
# ndarray 的数据类型  
def data_types_of_ndarray():
    print(f"{speter*2}data_types_of_ndarray{speter*2}")
    arr1 = np.array([1, 2, 3], dtype=np.float64)
    arr2 = np.array([1, 2, 3], dtype=np.int32)
    p_info(arr1dtype=arr1.dtype, arr2dtype=arr2.dtype)
        
    arr = np.array([1, 2, 3, 4, 5])

    float_arr = arr.astype(np.float64)
    p_info(arrdtype=arr.dtype, float_arrdtype=float_arr.dtype)
    
    arr3 = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])

    int_arr = arr3.astype(np.int32)
    p_info(arr3=arr3)
    p_info(int_arr=int_arr)
    
    numeric_strings = np.array(["1.25", "-9.6", "42"], dtype=np.bytes_)
    p_info(numeric_strings=numeric_strings.astype(float))
    
    int_array = np.arange(10)
    calibers = np.array([.22, .270, .357, .380, .44, .50], dtype=np.float64)
    p_info(int_array=int_array,calibers=calibers,result=int_array.astype(calibers.dtype))
    
    empty_array = np.empty(10, dtype="u4")
    zeros_array = np.zeros(10, dtype="u4")

    p_info(empty_array=empty_array)
    p_info(zeros_array=zeros_array)
    
# NumPy 数组算术  
def numpy_array_arithmetic():
    print(f"{speter*2}numpy_array_arithmetic{speter*2}")
    arr = np.array([[1., 2., 3.], [4., 5., 6.]])
    p_info(arr=arr, 乘=arr * arr,减=arr - arr)

    p_info(标量计算1=1/arr, 标量计算2=arr**0.5)
    
    arr2 = np.array([[0., 4., 1.], [7., 2., 12.]])
    p_info(arr2=arr2, 比较=arr2 > arr)
    
# 基础索引与切片  
def basic_indexing_slicing():
    print(f"{speter*2}basic_indexing_slicing{speter*2}")

    arr = np.arange(10)
    p_info(arr=arr, arr_5=arr[5], arr_5_8=arr[5:8])
    
    arr[5:8] = 12
    p_info(arr=arr)
    
    arr_slice = arr[5:8]
    p_info(arr_slice=arr_slice)
    
    arr_slice[1] = 12345
    p_info(arr=arr)
    
    arr_slice[:] = 64
    p_info(arr=arr)
    
    arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    p_info(arr2d_2=arr2d[2], arr2d_0_2=arr2d[0][2], arr2s_02=arr2d[0, 2])
    arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
    p_info(arr3d=arr3d, arr3d_0=arr3d[0])
    old_values = arr3d[0].copy()
    arr3d[0] = 42
    p_info(arr3d=arr3d)
    arr3d[0] = old_values
    p_info(arr3d=arr3d)
    p_info(arr3d_1_0=arr3d[1, 0])
    x = arr3d[1]
    p_info(x=x,x_0=x[0])
    
    p_info(arr=arr)
    p_info(arr_1_6=arr[1:6])
    
    p_info(arr2d=arr2d)
    p_info(arr2d_2=arr2d[:2])
    
    p_info(多组切片=arr2d[:2,1:])
    p_info(第二行前两列=arr2d[1,:2])
    p_info(第三列前两行=arr2d[:2,2])
    p_info(高维切片=arr2d[:, :1])
    # 赋值
    arr2d[:2, 1:] = 0
    p_info(赋值=arr2d)
    
# 布尔索引  
def boolean_indexing():
    print(f"{speter*2}boolean_indexing{speter*2}")
    names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])
    data = np.random.randn(7, 4)
    p_info(names=names, data=data)
    
    p_info(bool=names=='Bob')
    p_info(bool_array=data[names=='Bob'])
    
    p_info(bool_array索引=data[names=='Bob', 2:])
    p_info(bool_array索引1=data[names=='Bob', 3])
    
    p_info(_bool=names!='Bob')
    p_info(_bool_array=data[~(names=='Bob')])
    
    
    cond = names == 'Bob'
    p_info(cond=data[~cond])
    
    mask = (names == "Bob") | (names == "Will")
    p_info(mask=mask)
    p_info(mask_data=data[mask])
    
    data[data < 0] = 0
    p_info(data_置零=data)
    
    data[names != "Joe"] = 7
    p_info(data_置7=data)
# 神奇索引  
def magic_index():
    print(f"{speter*2}magic_index{speter*2}")
    arr = np.zeros((8, 4))
    for i in range(8):
        arr[i] = i
    p_info(arr=arr)

    p_info(arr_4_3_0_6=arr[[4, 3, 0, 6]])
    p_info(arr_3_5_7=arr[[-3, -5, -7]])
    
    arr = np.arange(32).reshape((8, 4))
    p_info(arr=arr)
    p_info(arr1=arr[[1, 5, 7, 2], [0, 3, 1, 2]])
    
    p_info(arr2=arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])
    
# 数组转置和换轴  
def array_transposition_axis_swapping():
    print(f"{speter*2}array_transposition_axis_swapping{speter*2}")

# 通用函数：快速的逐元素数组函数  
def general_function_fast_element_wise_array_functions():
    print(f"{speter*2}general_function_fast_element_wise_array_functions{speter*2}")

# 使用数组进行面向数组编程  
def using_arrays_for_array_oriented_programming():
    print(f"{speter*2}using_arrays_for_array_oriented_programming{speter*2}")

# 将条件逻辑作为数组操作  
def treat_conditional_logic_as_array_operations():
    print(f"{speter*2}treat_conditional_logic_as_array_operations{speter*2}")

# 数学和统计方法  
def mathematics_and_statistical_methods():
    print(f"{speter*2}mathematics_and_statistical_methods{speter*2}")

# 布尔值数组的方法  
def methods_for_boolean_arrays():
    print(f"{speter*2}methods_for_boolean_arrays{speter*2}")

# 排序  
def test_sort():
    print(f"{speter*2}test_sort{speter*2}")

# 唯一值与其他集合逻辑  
def unique_values_and_other_set_logic():
    print(f"{speter*2}unique_values_and_other_set_logic{speter*2}")

# 使用数组进行文件输入和输出  
def using_arrays_for_file_input_output():
    print(f"{speter*2}using_arrays_for_file_input_output{speter*2}")

# 线性代数 
def linear_algebra():
    print(f"{speter*2}linear_algebra{speter*2}")

# 伪随机数生成  
def pseudorandom_number_generation():
    print(f"{speter*2}pseudorandom_number_generation{speter*2}")

# 示例：随机漫步  
def random_walk():
    print(f"{speter*2}random_walk{speter*2}")

# 一次性模拟多次随机漫步  
def simulate_multiple_random_walks_in_a_single_run():
    print(f"{speter*2}simulate_multiple_random_walks_in_a_single_run{speter*2}")



 
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        magic_index()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


