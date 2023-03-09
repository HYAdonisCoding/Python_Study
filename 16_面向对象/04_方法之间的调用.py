
class Dog:
    """狗🐶"""
    def info(self):
        """返回狗的具体信息"""
        return f'一只名字叫{self.name}的{self.age}岁{self.breed}'
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
d2 = Dog()
d2.name = '旺财' 
d2.breed = '中华田园犬'
d2.age = 3
d2.run()
d2.eat('骨头')

d3 = Dog()
d3.name = '拆哥' 
d3.breed = '哈士奇'
d3.age = 3
d3.run()
