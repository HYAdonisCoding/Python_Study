# 外部函数
def test1():
    k = 10
    
    # 内部函数
    def test2():
        k = 200
        def test3():
            nonlocal k
            k = 100
        test3()
        
    print(f'k = {k}')
    test2()
    print(f'k = {k}')
    
test1()

