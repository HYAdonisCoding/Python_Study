class Player(object):
    # 类属性
    numbers = 0
    levels = ['青铜', '白银', '黄金', '钻石', '王者']
    # 初始化函数（构造函数）
    def __init__(self, name, age, city, level):
        # 实例属性
        self._name = name
        self._age = age
        self._city = city
        if level not in self.levels:
            raise ValueError(f'Level must be in {Player.levels}')
        else:
            self._level = level
            
        Player.numbers += 1
    
    def show(self):
        print(f'我是荣耀王者的第{Player.numbers}个玩家，我的名字是{self._name},我今年{self._age},我来自{self._city},我的段位是{self._level}')
     
    @property
    def city(self):
        return self._city
    @city.setter
    def city(self, value):
        if len(value) > 20 or len(value) < 2:
            raise ValueError('Invalid city')
        self._city = value
        
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise ValueError('Invalid age, must be an integer')
        if value < 0 or value > 100:
            raise ValueError('Invalid age, must be between 0 and 100')
        self._age = value
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if value == self._name:
            raise ValueError('Invalid name, name must not equal current name.')
        if len(value) > 20 or len(value) < 2:
            raise ValueError('Invalid name')
        self._name = value
          
    def level_up(self):
        index = Player.levels.index(self.level)
        if index < len(Player.levels) - 1:
            self.level = Player.levels[index+1]
            
    def get_weapon(self, weapon):
        self.weapon = weapon
    
    def show_weapon(self):
        return self.weapon.show_weapon()
    
    
    # 类方法
    @classmethod
    def get_players(cls):
        print(f'荣耀王者的用户数量已经达到了{cls.numbers}人')
        
    @staticmethod
    def ivalid(**kwargs):
        if kwargs['age'] >= 18:
            return True
        return False
    
class VIP(Player):
    # 构造函数重写
    def __init__(self, name, age, city, level, coin):
        super().__init__(name, age, city, level)
        self._coin = coin
        
    # 实例方法重写
    def  show(self):
        print(f'我是荣耀王者的第{Player.numbers}个玩家，我的名字是{self._name},我今年{self._age},我来自{self._city},我的段位是{self._level},我的余额是{self._coin}')

    
class Weapon(object):
    numbers = 0
    max_damage = 10000
    levels = ['青铜', '白银', '黄金', '钻石', '王者']
    all_weapons = []
    
    def __init__(self, name, damage, level):
        self.name = name
        self.damage = damage
        self.level = level
        Weapon.numbers += 1
        if damage > Weapon.max_damage:
            raise ValueError(f"Damage max is {Weapon.max_damage}, try again later")
        elif level not in Weapon.levels:
            raise ValueError(f"level must be in {Weapon.levels}")
        Weapon.all_weapons.append(self)
    
    @classmethod
    def get_max_damage(cls):
        max_damage = 0
        for weapon in cls.all_weapons:
            if weapon.damage > max_damage:
                max_damage = weapon.damage
        return max_damage
    
    def show_weapon(self):
        for k, v in self.__dict__.items():
            print(k, v)
            
# 封装、继承、实例属性、类属性、实例方法、类方法、静态方法、
def test_Class():
    eason = VIP('Eason', 28, '北京', '黄金', 1000)
    eason.name = 'Eason Jack'
    eason.age = 30
    eason.city = '南京'
    gun = Weapon('gun', 100, '青铜')
    eason.get_weapon(gun)
    eason.show_weapon()
    eason.show()
    print(eason.__dict__)
    # gun.show_weapon()

# 多态
class Animail(object):
    def speak(self):
        print('Amimail is speaking.')
        
class Cat(Animail):
    def speak(self):
        print('喵喵')
        return super().speak()   
    
class Dog(Animail):
    def speak(self):
        print('旺旺')
        return super().speak()   
class Test(object):
    def speak(self):
        print('Test')
        
def speak(object):
    object.speak()

def polymorphic():
    animail = Animail()
    kitty = Cat()
    puppy = Dog()
    t = Test()
    speak(kitty)
    speak(puppy)
    speak(t)
    speak(animail)


if __name__ == '__main__':
    
    test_Class()