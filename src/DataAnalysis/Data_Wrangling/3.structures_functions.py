#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# 第二章 内建数据结构、函数及文件  



def list_to_dic():
    seq1 = ['name', 'age', 'height']
    seq2 = ['Eason', 18, 1.82]
    mapping = {}
    for key, value in zip(seq1, seq2):
        mapping[key] = value
    print(mapping)
    mapping = dict(zip(seq1, seq2))
    print(mapping)
    
def test_dic():
    empty_dict = {}
    d1 = {"a": "some value", "b": [1, 2, 3, 4]}
    print(d1)
    print(f"{speter*2}{speter*2}")
    d1[7] = "an integer"
    print(d1)
    print(f"{speter*2}{speter*2}")
    d1[5] = "some value"
    print(d1)
    print(f"{speter*2}{speter*2}")
    d1["dummy"] = "another value"
    print(d1)
    print(f"{speter*2}{speter*2}")
    del d1[5]
    print(d1)
    print(f"{speter*2}{speter*2}")
    ret = d1.pop("dummy")
    print(ret)
    print(f"{speter*2}{speter*2}")
    
    print(d1)
    print(f"{speter*2}{speter*2}")
    d1.update({'b': 'foo', 'c': 12})
    print(d1)
    print(f"{speter*2}{speter*2}")
    
def test_zip():
    seq1 = ["foo", "bar", "baz"]
    seq2 = ["one", "two", "three"]
    zipped = zip(seq1, seq2)
    print(list(zipped))
    seq3 = [False, True]
    print(list(zip(seq1, seq2, seq3)))
    for index, (a, b) in enumerate(zip(seq1, seq2)):
        print(f"{index}: {a}, {b}")
def set_default():
    words = ["apple", "bat", "bar", "atom", "book"]
    by_letter = {}

    for word in words:
        letter = word[0]
        if letter not in by_letter:
            by_letter[letter] = [word]
        else:
            by_letter[letter].append(word)

    print(by_letter )
    by_letter1 = {}
    for word in words:
        letter = word[0]
        by_letter1.setdefault(letter, []).append(word)
    print(by_letter1 )
    from collections import defaultdict
    by_letter3 = defaultdict(list)
    print(by_letter3 )
    for word in words:
        by_letter3[word[0]].append(word)
    print(by_letter3 )
def test_set():
    a = set([2, 2, 2, 1, 3, 3])
    b = {2, 2, 2, 1, 3, 3}
    print(a)
    print(b)
    print(f"{speter*2}union{speter*2}")
    a = {1, 2, 3, 4, 5}
    b = {3, 4, 5, 6, 7, 8}
    print(a.union(b))
    print(a | b)
    print(f"{speter*2}intersection{speter*2}")
    
    print(a.intersection(b))
    print(a & b)
    print(f"{speter*2}|={speter*2}")
    c = a.copy()
    print('c', c)
    c |= b
    print('c', c)
    print(f"{speter*2}&={speter*2}")
    d = a.copy()
    print('d', d)
    d &= b
    print('d', d)
    
    print(f"{speter*2}tuple{speter*2}")
    my_data = [1, 2, 3, 4]
    my_set = {tuple(my_data)}
    print(my_set)
    print(f"{speter*2}issubset{speter*2}")
    a_set = {1, 2, 3, 4, 5}
    print({1, 2, 3}.issubset(a_set))
    print(a_set.issuperset({1, 2, 3}))
    
# 列表推导式
def list_derivation_formula():
    print(f"{speter*2}列表推导式{speter*2}")
    strings = ["a", "as", "bat", "car", "dove", "python"]
    print([x.upper() for x in strings if len(x) > 2])
    unique_lengths = {len(x) for x in strings}
    print(unique_lengths)
    a = set(map(len, strings))
    print(a)
    loc_mapping = {value: index for index, value in enumerate(strings)}
    print('loc_mapping', loc_mapping)
    loc_mapping = {index: value  for index, value in enumerate(strings)}
    print('loc_mapping', loc_mapping)
    
    print(f"{speter*2}嵌套列表推导式{speter*2}")
    all_data = [["John", "Emily", "Michael", "Mary", "Steven"],
            ["Maria", "Juan", "Javier", "Natalia", "Pilar"]]
    names_of_interest = []
    for names in all_data:
        enough_as = [name for name in names if name.count("a") >= 2]
        names_of_interest.extend(enough_as)
    print(names_of_interest)
    
    some_tuples = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    flattened = [x for tup in some_tuples for x in tup]
    print(flattened)
    
# 函数  
def test_function():
    print(f"{speter*2}函数{speter*2}")
    def my_function(x, y, z=1.5):
        if z > 1:
            return z * (x + y)
        else:
            return z / (x + y)
    print(my_function(2, 3))

a = None
# 命名空间、作用域和本地函数  
def namespaces_scopes_local_functions():
    print(f"{speter*2}命名空间、作用域和本地函数{speter*2}")
    def bind_a_variable():
        global a
        a = []
    bind_a_variable()
    print(a)
# 返回多个值  
def return_multiple_values():
    print(f"{speter*2}返回多个值{speter*2}")
    def f():
        a= 5 
        b = 6 
        c = 7
        return a, b, c
    print(f())
# 函数是对象
def functions_are_objects():
    print(f"{speter*2}函数是对象{speter*2}")
    states = ["   Alabama ", "Georgia!", "Georgia", "georgia", "FlOrIda",
          "south   carolina##", "West virginia?"]
    import re

    def clean_strings(strings):
        result = []
        for value in strings:
            value = value.strip()
            value = re.sub("[!#?]", "", value)
            value = value.title()
            result.append(value)
        return result
    print(clean_strings(states))
    def remove_punctuation(value):
        return re.sub("[!#?]", "", value)

    clean_ops = [str.strip, remove_punctuation, str.title]

    def clean_strings(strings, ops):
        result = []
        for value in strings:
            for func in ops:
                value = func(value)
            result.append(value)
        return result
    print(clean_strings(states, clean_ops))
    
    for x in map(remove_punctuation, states):
        print(x)
# 匿名（Lambda）函数  
def anonymous_lambda_function():
    print(f"{speter*2}函数{speter*2}")
    def short_function(x):
        return x * 2

    equiv_anon = lambda x: x * 2
    print(equiv_anon(3))
    def apply_to_list(some_list, f):
        return [f(x) for x in some_list]

    ints = [4, 0, 1, 5, 6]
    print(apply_to_list(ints, lambda x: x * 2))
    
    strings = ["foo", "card", "bar", "aaaa", "abab"]
    strings.sort(key=lambda x: len(set(x)))
    print(strings)

# 柯里化：部分参数应用  
def curry_partial_parameter_application():
    print(f"{speter*2}柯里化{speter*2}")
    def add_numbers(x, y):
        return x + y
    add_f = lambda y: add_numbers(5, y)
    from functools import partial
    add_five = partial(add_numbers, 5)
    
# 生成器  
def test_enerator():
    print(f"{speter*2}生成器{speter*2}")
    def squares(n=10):
        print(f"Generating squares from 1 to {n ** 2}")
        for i in range(1, n + 1):
            yield i ** 2
    gen = squares()
    for x in gen:
        print(x , end=' ')
    gen = (x ** 2 for x in range(100))
    print(sum(x ** 2 for x in range(100)))
    print(dict((i, i ** 2) for i in range(5)))
    
    import itertools
    def first_letter(x):
        return x[0]

    names = ["Alan", "Adam", "Wes", "Will", "Albert", "Steven"]

    for letter, names in itertools.groupby(names, first_letter):
        print(letter, list(names)) # names is a generator
# 错误和异常处理  
def error_exception_handling():
    print(f"{speter*2}错误和异常处理{speter*2}")
    def attempt_float(x):
        try:
            return float(x)
        except:
            return x
    def attempt_float(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return x
    print(attempt_float("1.2345"))
    print(attempt_float("something"))
# 文件与操作系统  
from pathlib import Path

base_dir = Path(__file__).parent
def files_operating_systems():
    print(f"{speter*2}files_operating_systems{speter*2}")
    path = f'{base_dir}/examples/segismundo.txt'
    # f = open(path, encoding="utf-8")
    # for line in f:
    #     print(line)
    lines = [x.rstrip() for x in open(path, encoding="utf-8")]
    print(lines)
    # f.close()
    
# 字节与 Unicode 文件 
def byte_unicode_files():
    print(f"{speter*2}byte_unicode_files{speter*2}")
    path = f'{base_dir}/examples/segismundo.txt'
    with open(path, mode="rb") as f:
        data = f.read(10)
    print(data)
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        byte_unicode_files()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


