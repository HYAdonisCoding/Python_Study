class Dog:
    __count = 0

    def __init__(self, name, breed, age):
        # 声明并初始化属性（成员变量、实例变量）
        self.name = name
        self.age = age
        self.breed = breed
        Dog.__count += 1
        self.__no = Dog.__count

    def __str__(self):
        """返回狗的具体信息"""
        return f'【一只编号为{self.__no}, 名字叫{self.name}的{self.age}岁{self.breed}】'

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
d2 = Dog('拆哥', '旺财', 6)

for _ in range(3):
    Dog('宝哥', '土狗', 2)

d3 = Dog('拆哥', '旺财', 8)

print(d1)
print(d2)
print(d3)
