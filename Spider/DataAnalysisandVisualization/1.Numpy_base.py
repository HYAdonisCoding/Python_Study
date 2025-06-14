import numpy as np

def array_porperty():
    a = np.arange(20).reshape(4, 5)
    print('创建一个4行5列的数组')
    
    print(a)
    print("数组的轴数（维度）：", a.ndim)
    print("数组的形状：", a.shape)
    print("数组类型：", a.dtype.name)
    print("数组元素的大小：", a.itemsize)
    print("数组大小：", a.size)
    print("数组a类型：", type(a))
    b = np.array([6, 7, 8])
    print("数组b类型：", type(b))
    print(b)

def data_type():
    dt = np.dtype(np.int32)
    print("创建整形类型:", dt)
    dt = np.dtype(np.float64)
    print("创建浮点类型:", dt)
    dt = np.dtype(np.bool_)
    print("创建布尔类型:", dt)
    dt = np.dtype(np.complex128)
    print("创建复数类型:", dt)
    dt = np.dtype([("2018", np.str_), ("GDP", np.float64)])
    print("创建自定义类型:", dt)    
    
def init_array():
    # 使用empty创建
    dt = np.empty([2, 2], dtype=int)
    print(dt)
    
    # 使用array创建
    dt = np.array([1, 2, 3, 4, 5])
    print('数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    dt = np.array([1.5, 2.3, 3.4, 4, 5])
    print('数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    dt = np.array([1, 2, 3, 4, 5], dtype='f8')
    print('数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    dt = np.array([[1], [2]], dtype='complex')
    print('数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    print('*' * 30)
    
    # 使用array创建
    dt = np.zeros([3, 5], dtype=int)
    print('全为0数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    dt = np.ones([3, 5], dtype=float)
    print('全为1数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    print('*' * 30)
    
    # 使用linspace创建
    dt = np.linspace(30, 50, num=5)
    print('第一个数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    dt = np.linspace(30, 50, num=5, endpoint=False)
    print('第二个数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    dt = np.linspace(30, 50, num=5, retstep=True)
    print('第三个数组：')
    print(dt)
    
    print('*' * 30)
    
    # 使用lrandom.rand创建
    dt = np.random.rand(10)
    print('第1个数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    dt = np.random.rand(10)
    print('第2个数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    print('*' * 30)
    
    # 使用lrandom.randn创建
    dt = np.random.randn(3, 5)
    print('符合正态分布的数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    print('*' * 30)
    
    # 使用lrandom.randint创建
    dt = np.random.randint(10, 30, 5)
    print('按范围随机产生的数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
    print('*' * 30)
    
    # 使用fromfunction创建
    dt = np.fromfunction(lambda i, j: i+j, (4, 5), dtype=int)
    print('按函数规则产生的数组：')
    print(dt)
    print('数组数据类型：', dt.dtype)
    
def base_operation():
    print('-' * 50)
    a = np.array([10, 20, 30, 40, 50])
    b = np.arange(5)
    print(f'a: {a}')
    print(f'b: {b}')
    c = a + b
    print(f'数组相加：\n{c}')
    c = a * b
    print(f'数组相乘：\n{c}')
    
    
    print('-' * 50)
    a_matrix = np.array([[1, 1], [1, 1]])
    b_matrix = np.array([[2, 0], [3, 4]])
    print(f'a_matrix: \n{a_matrix}')
    print(f'b_matrix: \n{b_matrix}')
    
    print(f'同一位置相乘：\n{a_matrix * b_matrix}')
    print(f'矩阵乘法：\n{a_matrix @ b_matrix}')
    print(f'矩阵乘法：\n{a_matrix.dot(b_matrix)}')
    
    print('-' * 50)
    print('索引、切片和迭代')
    a = np.arange(10)
    print(a)
    print(f'通过下标选择元素: \n{a[5]}')
    print(f'通过切片选择元素: \n{a[3:8]}')
    print(f'通过切片设置步长选择元素: \n{a[::2]}')
    print('循环数组：')
    for i in a:
        print(f'当前元素是：{i}')
    
    print('-' * 50)
    print('多维数组')
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(3, 4)
    print(a)
    print(f'通过下标选择元素: \n{a[2, 3]}')
    print(f'通过行切片选择指定列: \n{a[0:3, 2]}')
    print(f'通过行切片选择所有列: \n{a[0:2, :]}')
    print(f'通过列切片选择所有行: \n{a[:, 1:3]}')
    
    print('-' * 50)
    print('缺失索引')
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(3, 4)
    print(a)
    print(f'没有提供第二个维度索引，选取的数据: \n{a[2]}')
    
    print('-' * 50)
    print('三维数组')
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(2, 3, 2)
    print(a)
    print(f'三维数组的形状: \n{a.shape}')
    print(f'通过下标选择元素: \n{a[1, ...]}')
    
    print('-' * 50)
    print('三维数组的遍历')
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(2, 3, 2)
    print(a)
    for row in a:
        print(f'当前行数据: \n{row}')
    for el in a.flat:
        print(f'当前元素: \n{el}')
    
if __name__ == '__main__':
    base_operation()