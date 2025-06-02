#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
import sys
import types
def add1(item):
    if item == 1:
        return 1
    else:
        return item + add1(item - 1)
    
# 尾递归+生成器
def add_recursive(item, cur_compute_result=0):
    if item == 0:
        yield cur_compute_result
    else:
        yield from add_recursive(item - 1, cur_compute_result + item)

def add_recursive_generator(generator, item):
    gen = generator(item)
    return next(gen)
    
def func(a=None):
    if a is None:
        a = []
    a.append('hello')
    print(a)
    return a

# 传递可变参数
def func1(*args):
    count = 0
    for arg in args:    
        count += arg
    return count
# 传递关键字参数
def func2(**kwargs):
    tmp_list = []
    for k, v in kwargs.items():
        tmp_list.append(f"{k}={v}")
    return tmp_list
# 函数式编程
# 高阶函数
def func3(item):
    return item * 2

from functools import reduce
def func4(item1, item2):
    return item1 + item2

def use_reduce():
    # 使用reduce函数
    data = [1, 2, 3, 4, 5]
    data1 = reduce(func4, data)
    print(data1)  # Output: 15
    data1 = reduce(func4, data, 10000)  # Initial value set to 10000
    print(data1)  # Output: 15
    print(type(data1))  # Output: <class 'int'>
    # 使用lambda表达式
    data2 = reduce(lambda x, y: x + y, data)
    print(data2)  # Output: 15
    print(type(data2))  # Output: <class 'int'>
    # 使用生成器
    data3 = (x for x in data)
    data4 = reduce(func4, data3)
    print(data4)  # Output: 15
    print(type(data4))  # Output: <class 'int'>
    # 使用生成器表达式
    data5 = (x for x in range(1, 6))
    data6 = reduce(func4, data5)
    print(data6)  # Output: 15
    print(type(data6))  # Output: <class 'int'>
    # 使用生成器函数
    def generator_func():
        for x in range(1, 6):
            yield x
    data7 = generator_func()
    data8 = reduce(func4, data7)
    print(data8)  # Output: 15
    print(type(data8))  # Output: <class 'int'>
    # 使用生成器函数和yield
    def generator_func_yield():
        for x in range(1, 6):
            yield x
    data9 = generator_func_yield()
    data10 = reduce(func4, data9)
    print(data10)  # Output: 15
    print(type(data10))  # Output: <class 'int'>


def func5(item):
    if item % 2 == 0:
        return True
    
def use_filter():
    # 使用filter函数
    data = [1, 2, 3, 4, 5]
    data1 = filter(func5, data)
    print(data1)  # Output: <filter object at ...>
    print(type(data1))  # Output: <class 'filter'>
    print(list(data1))  # Output: [2, 4]
    
    # 使用lambda表达式
    data2 = filter(lambda x: x % 2 == 0, data)
    print(data2)  # Output: <filter object at ...>
    print(type(data2))  # Output: <class 'filter'>
    print(list(data2))  # Output: [2, 4]

def use_sort():
    # 使用sorted函数
    data = [5, 2, 3, 1, 4,-7, -3, -5, -1, -2]
    data1 = sorted(data)
    print('对列表进行排序，默认升序：',data1)  # Output: [1, 2, 3, 4, 5]
    data1 = sorted(data, reverse=True)
    print('对列表进行排序，降序：',data1)  # Output: [5, 4, 3, 2, 1]
    # 使用key参数
    data2 = sorted(data, key=abs)
    print('对列表进行排序，按照绝对值排序：',data2)  # Output: [1, 2, 3, 4, 5] - abs is not needed here as all are positive
    
    # 使用lambda表达式
    data2 = sorted(data, key=lambda x: -x)
    print(data2)  # Output: [5, 4, 3, 2, 1]
    
    # 使用reverse参数
    data3 = sorted(data, reverse=True)
    print(data3)  # Output: [5, 4, 3, 2, 1]
def use_lambda():
    # 使用lambda表达式
    data = [1, 2, 3, 4, 5]
    data1 = map(lambda x: x * 2, data)
    print(data1)  # Output: <map object at ...>
    print(type(data1))  # Output: <class 'map'>
    print(list(data1))  # Output: [2, 4, 6, 8, 10]
    data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data2 = map(lambda x: x * 2, data1)
    print(data2)  # Output: <map object at ...>
    print(type(data2))  # Output: <class 'map'>
    print(list(data2))  # Output: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    data1 = [('a', 11), ('b', -22), ('c', 23), ('d', -14)]
    print('使用lambda表达式对元组列表进行排序：', sorted(data1, key=lambda x: x[1]))
    # Output: [('b', -22), ('d', -14), ('a', 11), ('c', 23)]
    data1 = [{'key', 11}, {'key2', -22}, {'key3', 23}, {'key4', -14}]
    print('使用lambda表达式对字典列表进行排序：', sorted(data1, key=lambda x: x[1]))
    # Output: [{'key2', -22}, {'key4', -14}, {'key', 11}, {'key3', 23}]
    
import datetime
import time
#  装饰器
count = 5
def use_loop():
    
    
    def loop():
        time1 = datetime.datetime.now()
        for i in range(count):
            time.sleep(1)
        time2 = datetime.datetime.now()
        print(f"Loop completed in {(time2 - time1).seconds} seconds")

    loop()

def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function '{func.__name__}' with arguments: {args} and keyword arguments: {kwargs}")
        
        time1 = datetime.datetime.now()
        func(*args, **kwargs)
        time2 = datetime.datetime.now()
        print(f"Function '{func.__name__}' 循环耗时: {(time2 - time1).seconds} seconds")
    return wrapper
@log
def add_with_log():
    print(f"Adding recursively")
    for _ in range(count):
        time.sleep(1)
     
# 偏函数
from functools import partial

def fun(a, b, c, d, e):
    return a + b + c + d + e
def use_partial():
    partial_func = partial(fun, 2, 3, 4, 5)  
    result = partial_func(10)
    print(f"Partial function result: {result}")  # Output: 24

def fun1():
    global var1, var2, var3
    var1 = 100
    var2 = 200
    var3 = 300
    var4 = 400
    print(f"func1的局部变量 variables: var1:{var1}, var2:{var2}, var3:{var3}, var4:{var4}")
def use_global():
    fun1()
    print(f"全局变量 variables: var1:{var1}, var2:{var2}, var3:{var3}")
    # print(f"输出变量 variables: var4:{var4}")  # var4 is not defined in this 
    print('所有的全局变量', globals())

# 闭包
def fun2():
    local_var = [0]
    
    def fun1():
        local_var[0] += 1
        print(f"闭包函数的局部变量 local_var: {local_var[0]}")
        return local_var[0]
    return fun1
def use_Closure():
    closure_func = fun2()
    for _ in range(10):
        print('第%s次调用闭包函数:' % (_ + 1), closure_func())  # Output: 1, 2, 3 - each call increments the local variable in the closure
        
# 模块
import test1

def use_module():
    test1.show('这是recursion.py中的show函数')
    print('这是recursion.py中的show函数')
from test1 import show, add

import sys
sys.path.append('/Users/adam/Documents/Developer/MyGithub/Python_Study')

import DataAnalusispackage.time_tools as time_tools
@time_tools.log_comment('测试循环耗时')
def use_module1():
    show('这是recursion.py中的show函数')
    print('这是recursion.py中的add函数', add(1, 2))  # Output: 3
    for _ in range(5):
        time.sleep(1)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        print(f"After pass {i+1}: {arr}")  # Output: After pass 1: [34, 25, 12, 22, 11, 64, 90]
    return arr
def use_bubble_sort():
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted array:", data)  # Output: Unsorted array: [64, 34, 25, 12, 22, 11, 90]
    # 使用冒泡排序
    sorted_data = bubble_sort(data)
    print("Sorted array:", sorted_data)  # Output: Sorted array: [11, 12, 22, 25, 34, 64, 90]

# 创建抽象类
from abc import ABCMeta, abstractmethod

class Poultry(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def show(self):
        print(f"这是{self.name}的show函数")

def use_metaclass():
    class Chicken(Poultry):
        def __init__(self, name):
            super().__init__(name)

        def show(self):
            print(f"这是鸡的show函数，名字是{self.name}")
        colour = 'yellow'  # 类属性
        num = 1 # 类属性

    class Duck(Poultry):
        def __init__(self, name):
            super().__init__(name)

        def show(self):
            print(f"这是鸭的show函数，名字是{self.name}")
        # 若该类包含了抽象方法，则不能实例化
        # @abstractmethod
        # def run(self):
        #     pass
        
    
    chicken = Chicken("小鸡")
    duck = Duck("小鸭")
    chicken.show()  # Output: 这是鸡的show函数，名字是小鸡
    duck.show()     # Output: 这是鸭的show函数，名字是小鸭    
    print("对象的地址:", id(chicken))  # Output: 对象的地址: <some_id>
    print("对象的类型:", type(chicken))  # Output: 对象的类型: <class '__main__.Chicken'>
    print("对象的地址:", id(duck))     # Output: 对象的地址: <some_id>
    print("对象的类型:", type(duck))     # Output: 对象的类型: <class '__main__.Duck'>
    print("通过类名访问属性:colour", Chicken.colour)  # Output: yellow
    print("通过类名访问属性:num", Chicken.num)  # Output: 1
    
    print("通过实例访问属性:colour", chicken.colour)  # Output: yellow
    print("通过实例访问属性:num", chicken.num)  # Output: 1
    chicken1 = Chicken("小鸡")
    print("chicken1 的colour地址:", id(chicken1.colour))  # Output: 小鸡
    print("chicken1 的num地址:", id(chicken1.num))  # Output: 1
    chicken1.name = "小鸡1"
    print("chicken 的colour地址:", id(chicken.colour))  # Output: 小鸡
    print("chicken 的num地址:", id(chicken.num))  # Output: 1
    Chicken.colour = 'red'  # 修改类属性
    Chicken.num = 2  # 修改类属性
    print("chicken1 的colour地址:", id(chicken1.colour))  # Output: 小鸡
    print("chicken1 的num地址:", id(chicken1.num))  # Output: 1
    
    print("chicken 的colour地址:", id(chicken.colour))  # Output: 小鸡
    print("chicken 的num地址:", id(chicken.num))  # Output: 1

def use_attribute():
    class Chicken():
        def __init__(self, name, weight, price):
            self._name = name
            self.weight = weight
            self.price = price

        def show(self):
            print(f"这是鸡的show函数，名字是{self.name}")
        colour = 'yellow'  # 类属性
        num = 1 # 类属性  
        
        @property
        def weight(self):
            return self._weight
        @weight.setter
        def weight(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("Weight must be a number")
            if value < 0.1 or value > 12.0:
                raise ValueError("Weight cannot be negative(< 0.1) or greater than 12.0")
            
            self._weight = value
        # 实例方法
        # def fly(self):
        #     print("小鸡: {0} is flying".format(self._name))
        def run(self):
            
            print("小鸡: {0} is running".format(self._name))
        # 静态方法
        # @staticmethod
        # def get_colour():
        #     print("小鸡颜色：{0}".format(Chicken.colour))
        @staticmethod
        def go_run(num):
            print("小鸡跑了{0}米".format(num))
        # 类方法
        @classmethod
        def get_colour(cls):
            print('cls:', cls)
            # cls是类本身
            print("小鸡颜色：{0}".format(cls.colour))
        
        # 抽象方法
        # 不能实例化包含抽象类的抽象方法
        @abstractmethod
        def fly(self):
            print("小鸡: {0} is flying".format(self._name))
        
    def swim(num):
        print("小鸡: {0} is swimming".format(num))
        
    Chicken.swim = swim  # 动态添加实例方法
    Chicken.swim(5)  # Output: 小鸡: 5 is swimming
    Chicken.get_colour()  # Output: 小鸡重量：yellow
    Chicken.go_run(10)  # Output: 小鸡跑了10米
    chicken1 = Chicken("小鸡", 1.5, 10.0)  
    chicken2 = Chicken("小鸡2", 1.5, 10.0)
    chicken1.get_colour()  # Output: 小鸡颜色：yellow
    chicken2.fly()  # Output: 小鸡2 0 is flying
    chicken2.run()  # Output: 小鸡2 0 is running
    try:
        print(Chicken.colour)  # Output: yellow
        # print(Chicken.price)  # Output: 1
        chicken1.weight = '10'  # 设置实例属性
    except Exception as e:
        print(f"通过类名访问实例属性 触发异常: {e}")
    # 适用场景
    # 根据实例方法、静态方法和类方法、抽象方法、动态方法的运行原理的不同总结适用场景：
    # 1. 实例方法（Instance Method）定义方式：第一个参数为 self。适用场景：需要访问或修改实例属性、实例状态时使用。
    # 2. 静态方法（Static Method）定义方式：不需要 self 或 cls。适用场景：不需要访问实例属性或类属性时使用。
    # 3. 类方法（Class Method）定义方式：第一个参数为 cls。适用场景：需要访问或修改类属性时使用。
    # 4. 抽象方法（Abstract Method）定义方式：使用 @abstractmethod 装饰器。适用场景：在抽象类中定义接口，要求子类必须实现该方法。
    # 5. 动态方法（Dynamic Method）定义方式：在类定义后动态添加。适用场景：需要在运行时添加方法或功能时使用。
# 类的继承
def use_inheritance():
    class Poultry():
        def __init__(self, name):
            self.name = name
        
        def show(self):
            print(f"父类：这是{self.name}的show函数")
    class Chicken():
        def __init__(self, name):
            super().__init__(name)
    
        def show(self):
            print(f"这是鸡的show函数，名字是{self.name}")
        def eat(self):
            print(f"父类：鸡{self.name}正在吃东西")
    
    class Cock(Poultry, Chicken):
        def __init__(self, name):
            super().__init__(name)
    cock = Cock('黄色')
    print('访问_name属性：', cock.name)
    cock.show()
    cock.eat()
    
# 多态
def use_Polymorphism():
    class Poultry():
        def __init__(self, name):
            self.name = name
        
        def show(self):
            print(f"父类：这是{self.name}的show函数")
    class Chicken():
        def __init__(self, name):
            super().__init__(name)
    
        def show(self):
            print(f"这是鸡的show函数，名字是{self.name}")
        def eat(self):
            print(f"父类：鸡{self.name}正在吃东西")
    
    class Cock(Poultry, Chicken):
        def __init__(self, name):
            super().__init__(name)
        def show(self):
            print(f'这是子类：{self.__class__.__name__}的show方法')
        def eat(self):
            print('这是子类调用')
            return super().eat()
    cock = Cock('黄色')
    print('访问_name属性：', cock.name)
    cock.show()
    cock.eat()
# 可调用对象
def use_Callable_Objects():
    class WildGoose:
        def __call__(self, direction):
            print(f'大雁正往 {direction} 方向飞')
            
    wild_goose = WildGoose()
    wild_goose('南')
    
def use_Callable_Objects1():
    class WildGoose:
        def __init__(self):
            self.direction = []
            self.colour = '白色'
            self.weight = '10kg'
            
        def __call__(self, direction):
            self.direction.append(direction)
            print(f'大雁正往 {direction} 方向飞')
        def __str__(self):
            return str.join("--->", self.direction)
    wild_goose = WildGoose()
    # wild_goose('上海')
    # wild_goose('杭州')
    # wild_goose('南京')
    # wild_goose('广州')
    # wild_goose('北京')
    # print('大雁飞行轨迹：', str(wild_goose))
    wild_goose.name = '鸿雁'
    print('wild_goose的对象属性：', wild_goose.__dict__)
    del wild_goose.name
    print('wild_goose的对象属性：', wild_goose.__dict__)
def use_Callable_Objects2():
    class WildGoose:
        """大雁类"""
        __slots__ = ['direction', 'colour', 'weight']
        # 使用__slots__来限制属性
        # 这样可以节省内存并提高性能，尤其是在创建大量实例时
        # 但不能动态添加属性
        def __init__(self):
            self.direction = []
            self.colour = '白色'
            self.weight = '10kg'
            
        def __call__(self, direction):
            self.direction.append(direction)
            print(f'大雁正往 {direction} 方向飞')
        def __str__(self):
            return str.join("--->", self.direction)
        def fly(self):
            print(f'大雁正在飞行，方向为：{self.direction}')
    wild_goose = WildGoose()
    print('wild_goose的对象属性：', wild_goose.__slots__)
    # wild_goose.name = '鸿雁'
    # print('wild_goose的对象属性：', wild_goose.__slots__)
    # 反射机制
    fly = getattr(wild_goose, 'fly', None)
    fly()

# 快速赋值
def use_quick_assignment():
    class Person:
        
        def __init__(self, ID, name, age, height, weight):
            self._ID = ID
            self._height = height
            self._weight = weight
            
            self._name = name
            self._age = age

        def __str__(self):
            return f"Person(name={self._name}, age={self._age}, height={self._height}, weight={self._weight})"
    # 快速赋值
    person1 = Person(ID=1, name='张三', age=25, height=175, weight=70)
    print(f"person1: {person1}")  # Output: Person(name=张三, age=25, height=175, weight=70)
    person2 = Person(ID=2, name='李四', age=30, height=180, weight=75)
    print(f"person2: {person2}")  # Output: Person(name=李四, age=30, height=180, weight=75)
    p_list = ['_ID', '_age', '_height', '_weight']
    # 使用快速赋值
    for i in p_list:
        if hasattr(person1, i):
            val = getattr(person1, i)
            setattr(person2, i, val)
    print(f"person2 after quick assignment: {person2}")  # Output: Person(name=张三, age=25, height=175, weight=70)
# 多继承中不同基类有同名方法，子类继承哪一个？
def use_multiple_inheritance():
    class Poultry:
        def eat(self):
            print("Poultry is eating")
    class Chicken:
        def eat(self):
            print("Chicken is eating")
    class Cock(Poultry, Chicken):
        pass
    class Cock1(Chicken, Poultry):
        pass
    c1 = Cock()
    c1.eat()
    c2 = Cock1()
    
    c2.eat()
# 设计算法，构造一棵二叉树
import random

def use_TreeNode():
    class TreeNode:
        
        def __init__(self, name, value):
            self._value = value
            self._name = name
            self._left_node = None
            self._right_node = None
        def __str__(self):
            left = self._left_node._name if self._left_node else None
            right = self._right_node._name if self._right_node else None
            return f"TreeNode({self._name}, value={self._value}, left={left}, right={right})"
    class Tree:
        root = None
        nodes = []
        def add_node(self, name, index, value=None):
            node = TreeNode(name, value)
            print(f"添加节点: {name} (index={index}, value={value})")
            if self.root is None:
                self.root = node
                self.nodes.append(node)
                print(f"设置根节点: {node._name}")
            else:
                parent_index = (index - 1) // 2
                tmp_node = self.nodes[parent_index]
                if not tmp_node._left_node:
                    tmp_node._left_node = node
                    print(f"{tmp_node._name} 的左子节点 -> {node._name}")
                else:
                    tmp_node._right_node = node
                    print(f"{tmp_node._name} 的右子节点 -> {node._name}")
                self.nodes.append(node)

        def print_tree(self):
            print("\n当前所有节点：")
            for node in self.nodes:
                print(node)
        

    def print_tree_ascii(node, prefix="", is_left=True):
        """递归打印二叉树结构（文本版，带 value）"""
        if node is not None:
            connector = "├── " if is_left else "└── "
            print(prefix + connector + f"{node._name} (value={node._value})")
            # 判断是否有子节点，准备新的前缀
            if node._left_node or node._right_node:
                if node._left_node:
                    # 如果有右节点，左节点前缀用 │，否则用空格
                    next_prefix = prefix + ("│   " if node._right_node else "    ")
                    print_tree_ascii(node._left_node, next_prefix, True)
                if node._right_node:
                    next_prefix = prefix + "    "
                    print_tree_ascii(node._right_node, next_prefix, False)
    tree = Tree()
    all_node = ['Root', 'Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6', 'Node7', 'Node8', 'Node9', 'Node10']
    
    for i, val in enumerate(all_node):
        tree.add_node(val, i, random.randint(1, 100))
    print_tree_ascii(tree.root)
if __name__ == "__main__":
    use_TreeNode()
    # time_tools.log(use_module1, '这是装饰器参数')()

    # 使用高阶函数
    # data = [1, 2, 3, 4, 5]
    # data1 = map(func3, data)
    # print(data1)  # Output: [2, 4, 6, 8, 10]
    # print(type(data1))  # Output: <class 'map'>
    # print(tuple(data1))  # Output: () - empty because map object is exhausted
    # data = [1, 2, 3, 4, 5]
    # print(func1(*data))  # Output: 15
    # data = (1, 3, 5, 7, 9)
    # print(func1(*data))  # Output: 25
    # dic = {"key1": "value1", "key2": "value2"}
    # print(func2(**dic))  # Output: ['key1=value1', 'key2=value2']
    # print(add(5))  # Output: 15
    # print(add(10))  # Output: 55
    # print(add(100))  # Output: 5050
    
    # sys.setrecursionlimit(2000)  # Increase recursion limit for larger inputs
    
    # print(add(1000))  # Output: 500500
    # print(add_recursive_generator(add_recursive, 10000))  # Output: 50005000
    # func()  # Output: ['hello']
    # func()  # Output: ['hello', 'hello']
    # func()  # Output: ['hello', 'hello', 'hello']