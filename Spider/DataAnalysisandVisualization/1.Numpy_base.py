import numpy as np
# 9.1 NumPy基础
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

# 9.2 形状操作

def change_shape():
    a = np.floor(10 * np.random.random((4, 5)))
    
    print(f'原始数组形状: \n{a.shape}')
    
    print('-' * 50)
    
    b = a.ravel()
    print(f'将多维数组转为一维数组b:\n{b}\n新数组形状: \n{b.shape}')
    
    print('-' * 50)
    c = a.reshape(2, 10)
    print(f'将数组转为指定形状c:\n{c}\n新数组形状: \n{c.shape}')
    
    d = a.T
    print(f'将数组进行行列转换(矩阵转置): \n{d.shape}')
    
    print('-' * 50)
    a = np.floor(10 * np.random.random((4, 5)))
    print(f'修改之前形状为: \n{a.shape}')
    a.resize(2, 10)
    print(f'修改之后形状为: \n{a.shape}')
    
    # 数组堆叠
    print('-' * 50, '数组堆叠', '-' * 50)
    a = np.floor(10 * np.random.random((2, 10)))
    print(f'数组a: \n{a}')
    
    b = np.floor(10 * np.random.random((2, 10)))
    print(f'数组b: \n{b}')
    
    c = np.vstack((a, b))
    print(f'沿垂直方向堆叠c: \n{c}')
    
    d = np.hstack((a, b))
    print(f'沿水平方向堆叠d: \n{d}')
    
    print('-' * 50, 'column_stack将一维数组堆叠到二维数组中', '-' * 50)
    a = np.floor(10 * np.random.random((2)))
    print(f'数组a: \n{a}')
    
    b = np.floor(10 * np.random.random((2)))
    print(f'数组b: \n{b}')
    
    c = np.column_stack((a, b))
    print(f'沿垂直方向堆叠c: \n{c}')
    
    d = np.column_stack((a[:, np.newaxis], b[:, np.newaxis]))
    print(f'添加新轴然后进行堆叠d: \n{d}')
    
    print('-' * 50, '矩阵拆分', '-' * 50)
    a = np.floor(10 * np.random.random((2, 20)))
    print(f'数组a: \n{a}')
    print('水平方向拆分')
    data = np.hsplit(a, 2)
    for item in data:
        print(item)
        
    print('垂直方向拆分')
    data = np.vsplit(a, 2)
    for item in data:
        print(item)
    print('拆分成指定大小的数组')
    data = np.array_split(a, 2)
    for item in data:
        print(item)
    print('-' * 50, '副本', '-' * 50)
    
    a = np.arange(16)
    b = a
    if b is a:
        print('b == a')
    print(f'a的地址: \n{id(a)}')
    print(f'b的地址: \n{id(b)}')
    b.shape = 4, 4
    print(f'a的形状: \n{a.shape}')
    
    print(f'b的形状: \n{b.shape}')
    
    print('-' * 50, '浅拷贝', '-' * 50)
    
    a = np.arange(16)
    b = a.view()
    if b is a:
        print('b 和 a 是同一个对象')
    else:
        print('b 和 a 不是同一个对象')
        
    print(f'a的地址: \n{id(a)}')
    print(f'b的地址: \n{id(b)}')
    
    print(f'判断b的base是否和a一样: \n{b.base is a}')
    print(f'判断b是否存在独立的一份数据拷贝: \n{b.flags.owndata}')
    print(f'修改b的形状{(4, 4)}')
    b.shape = 4, 4
    print(f'a的形状: \n{a.shape}')
    
    print(f'b的形状: \n{b.shape}')
    print(f'修改b的数据:b[0, 2] = 10')
    b[0, 2] = 10
    print(f'查看a的数据: \n{a}')
    print('数组切片')
    c = a[1:3]
    c[1] = 200
    print(f'修改切片后的数据，然后查看对a的影响: \n{a}')
    
    print('-' * 50, '深拷贝', '-' * 50)
    
    a = np.arange(16)
    b = a.copy()
    if b is a:
        print('b 和 a 是同一个对象')
    else:
        print('b 和 a 不是同一个对象')
        
    print(f'a的地址: \n{id(a)}')
    print(f'b的地址: \n{id(b)}')
    b[5] = 200
    print(f'a的地址: \n{a}')
    print(f'b的地址: \n{b}')
    
    print(f'判断b的base是否和a一样: \n{b.base is a}')
    print(f'判断b是否存在独立的一份数据拷贝: \n{b.flags.owndata}')
    
# 9.4 高级索引
def advanced_Indexing():
    print('-' * 50, '通过数组索引', '-' * 50)
    
    a = np.arange(10) * 2
    print(f'原始数组a: \n{a}')
    b = np.array([1, 1, 3, 4])
    print(f'通过b索引的数据: \n{a[b]}')
    
    c = np.array([[2, 3], [5, 6],[7, 8]])
    print(f'通过c索引的数据: \n{a[c]}')
    
    data = np.array([[0, 0, 0, 99],
                    [168, 0, 0, 23],
                    [0, 198, 0, 78],
                    [0, 0, 23, 64],
                    [121, 0,88, 36]])
    index = np.array([[1, 2, 3, 4], [0, 2, 1, 3]])
    print(f'data:\n{data}, \n\nindex:\n{index},\n\ndata[index]:\n{data[index]}')
    
    print('-' * 50, '对于一维数组提供索引，每个维度的索引数必须相同', '-' * 50)
    
    a = (np.arange(16) * 2).reshape(4, 4)
    print(f'原始数组a: \n{a}')
    
    b = np.array([[0, 1], [2, 3]])
    c = np.array([[1, 2], [3, 3]])
    
    print(f'两个维度都使用二维数组索引: \n{a[b, c]}')
    print(f'第一个维度都使用二维数组索引: \n{a[b, 1]}')
    print(f'第二个维度都使用二维数组索引: \n{a[:, b]}')
    
    print('-' * 50, '数组索引：检索数组的极值', '-' * 50)
    
    a = (np.sin(np.arange(12) * 10)).reshape(4, 3)
    print(f'原始数组a: \n{a}')
    
    max_val_posi = a.argmax(axis=0)
    print(f'每列上最大值的位置: \n{max_val_posi}')
    
    data_max = a[max_val_posi, range(3)]
    print(f'检索最大值，并返回新的数组: \n{data_max}')
    
    print('-' * 50, '通过布尔索引', '-' * 50)
    
    a = np.arange(8).reshape(2, 4)
    print(f'原始数组a: \n{a}')
    
    b = a > 4
    print(f'新的布尔数组b: \n{b}')
    
    print(f'使用布尔数组进行筛选: \n{a[b]}')
    
    a = np.arange(8).reshape(2, 4)
    print(f'原始数组a: \n{a}')
    
    b1 = np.array([False, True])
    b2 = np.array([True, False, True, False])
    print(f'选取第一维第二行和所有列: \n{a[b1, :]}')
    
    print(f'选取第一维第二行和第二维第一、三列: \n{a[b1, b2]}')
    
    print('-' * 50, '通过ix()函数索引', '-' * 50)
    
    a = np.arange(10).reshape(2, 5)
    print(f'原始数组a: \n{a}')
    
    b = np.ix_([0, 1], [2, 3])
    print(f'使用整数数组筛选数据: \n{a[b]}')
    c = np.ix_([True, True], [1, 3])
    print(f'使用布尔数组筛选数据: \n{a[c]}')
if __name__ == '__main__':
    advanced_Indexing()