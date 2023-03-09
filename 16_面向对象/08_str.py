class Dog:
    def __init__(self, name=None, breed=None, age=None):
        # 声明并初始化属性（成员变量、实例变量）
        self.name = name
        self.age = age
        self.breed = breed
    def __str__(self):
        """返回狗的具体信息"""
        return f'【一只名字叫{self.name}的{self.age}岁{self.breed}】'
    
    def run(self):
        """
        让一只狗跑步
        :param name: 名字
        :param breed: 品种
        :param age: 年龄
        """
        print(f'{self}跑起来了')
    def eat(self, food):
        """
        让狗吃东西
        :param food: 食物
        """
        print(f'{self}吃了{food}')
        
d1 = Dog('宝哥', '柴犬', 5)
print(d1)
print(str(d1))
d1.run()
d1.eat("花生米")

print(d1.__dict__)

print('-' * 30)

