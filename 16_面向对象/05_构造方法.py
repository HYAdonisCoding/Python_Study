class Dog:
    def __init__(self):
        # 声明并初始化属性（成员变量、实例变量）
        self.name = None
        self.age = None
        self.breed = None
    def info(self):
        """返回狗的具体信息"""
        return f'【一只名字叫{self.name}的{self.age}岁{self.breed}】'
    def run(self):
        """
        让一只狗跑步
        :param name: 名字
        :param breed: 品种
        :param age: 年龄
        """
        print(f'{self.info()}跑起来了')
    def eat(self, food):
        """
        让狗吃东西
        :param food: 食物
        """
        print(f'{self.info()}吃了{food}')
        
d1 = Dog()
d1.name = '宝哥' 
d1.breed = '柴犬'
d1.age = 5
d1.run()
d1.eat("花生米")

# 类的作用？
# 描述、模拟一种事物类型

# 存在的问题
# 1.从class代码里面看不出有哪些属性
# 2.属性名没有任何提示
# 3.不同的对象可以拥有不同数量的属性
# 4.在方法中访问对象属性时会有警告