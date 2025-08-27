class Dog:
    def __init__(self, name=None, breed=None, age=None):
        # 声明并初始化属性（成员变量、实例变量）
        self.name = name
        self.age = age
        self.breed = breed
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
        
d1 = Dog('宝哥', '柴犬', 5)
d1.run()
d1.eat("花生米")

d2 = Dog('宝哥2', '柴犬2',None)
d2.run()
d2.eat("骨头")

d3 = Dog('宝哥3', '柴犬2', 5)
d3.run()
d3.eat("火腿")
# 类的作用？
# 描述、模拟一种事物类型

# 存在的问题
# 1.从class代码里面看不出有哪些属性
# 2.属性名没有任何提示
# 3.不同的对象可以拥有不同数量的属性
# 4.在方法中访问对象属性时会有警告