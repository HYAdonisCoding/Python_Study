'''
学生管理系统
学生
老师
班级
课程
'''
class User(object):
    def __init__(self, name, age, gender, id_number) -> None:
        self.__name__ = name
        self.__age__ = age
        self.__gender__ = gender
        self.__id_number__ = id_number
    
    def show_infos(self):
        print('*'*5 + '基本信息' + '*'*5)
        print(f'''
    姓名：{self.__name__}
    年龄：{self.__age__}
    性别：{self.__gender__}
    编号：{self.__id_number__}''')
        
class Student(User):
    def __init__(self, name, age, gender, id_number) -> None:
        super().__init__(name, age, gender, id_number)
        self.__courses__ = []
    def show_infos(self):
        super().show_infos()
        
        print('选课信息：')
        if self.__courses__ == []:
            print('未选课')
        else:
            for course in self.__courses__:
                print(course.name)
        print('*'*30)
                
    def add_course(self, course):
        self.__courses__.append(course)
class Teacher(User):
    def __init__(self, name, age, gender, id_number, assistant, cla) -> None:
        super().__init__(name, age, gender, id_number)
        self.__assistant__ = assistant
        self.__cla__ = cla
    
    def show_infos(self):
        super().show_infos()
        print(f'是否是辅导员：{["否", "是"][self.__assistant__]}')
        print('辅导班级：')
        if not self.__cla__:
            print('暂无')
        else:
            for info in self.__cla__:
                print(info)
        print('*'*30)
class Cla(object):
    def __init__(self, name, id_number, teacher, students) -> None:
        self.__name__ = name
        self.__id_number__ = id_number
        self.__students__ = students
        self.__teacher__ = teacher
    
    def show_infos(self):
        print('*'*15 + '班级信息' + '*'*15)
        print(f'班级名称：{self.__name__}')
        print(f'班级班号：{self.__id_number__}')
        print(f'班级辅导员：{self.__teacher__.__name__}')
        print('学生信息：')
        if not self.__students__:
            print('空')
        else:
            for student in self.__students__:
                print(student.__name__)
        print('*'*15 + '班级信息' + '*'*15)
        
    def add_student(self, student):
        if student in self.__students__:
            raise Exception('Student is already in this Class')
        else:
            self.__students__.append(student)
            return True
    
    def sub_student(self, student):
        if student in self.__students:
            self.__students__.remove(student)
            return True
        else:
            raise Exception('Student is not in this Class')
class Course():
    # 属性：课名、课程id、老师、学生列表、课程性质、课程容量
    courses = [] # 累属性
    def __init__(self, name, id_number, teacher, students, type, number) -> None:
        self.__name__ = name
        self.__id_number__ = id_number
        self.__students__ = students
        self.__type__ = type
        self.__number__ = number
        self.__teacher__ = teacher
        self.student_number = len(self.__students__)
        self.valid_number = self.__number__ - self.student_number
        Course.courses.append(self.__name__)
        
    @property
    def name(self):
        return self.__name__
    @name.setter
    def name(self, newName):
        if not isinstance(newName, str):
            raise TypeError('newName must be a string')
        if len(newName)>40 or len(newName)<3:
            raise ValueError('newName must be between 3 and 40 characters')
        self.__name__ = newName
        
    def show_infos(self):
        print(f"{'*'*20} 课程信息 {'*'*20}")
        print(f"课程名称：{self.__name__}")
        print(f"课程编号：{self.__id_number__}")
        print(f"授课教师：{self.__teacher__.__name__}")
        print(f"{self.__type__}")
        print(f"课程容量：{self.__number__}")
        print(f"已选学生人数：{self.student_number}")
        print(f"剩余学生空位：{self.valid_number}")
        print("学生信息：")
        
        if not self.__students__:
            print("空")
        else:
            for student in self.__students__:
                print(student.__name__)
    
    def add_student(self, student):
        if student in self.__students__:
            raise ValueError('Student is already in the Classroom')
        if self.valid_number == 0:
            raise Exception('This course has no students')
        self.__students__.append(student)
        self.valid_number -= 1
        self.student_number += 1
        student.add_course(self)
        return True
    def sub_student(self, student):
        if student not in self.__students__:
            raise ValueError('Student is not in the Classroom')
        self.__students__.remove(student)
        self.valid_number += 1
        self.student_number -= 1
        return
    @classmethod
    def show_courseList(cls):
        return cls.courses
        
if __name__ == '__main__':
    # 创建学生对象
    jack = Student('Eason', 20, '男', 2401)
    rose = Student('Rose', 20, '女', 2402)
    lily = Student('Lily', 19, '女', 2403)
    # jack.show_infos()
    # 创建教师对象
    eason = Teacher('Eason', 30, '男', 1401, True, ['计算机一班', '网络二班'])
    tom = Teacher('Tom', 50, '女', 10401, False, [])
    # tom.show_infos()
    # 创建班级对象
    computer_1 = Cla('Computer', 101, eason, [])
    computer_2 = Cla('Computer Network', 102, eason, [jack, rose])
    # computer_1.show_infos()
    # computer_2.show_infos()
    # 创建课程对象
    python = Course('Python', 3, eason, [jack, rose], '必修课', 10)
    java = Course('Java', 3, eason, [jack, lily], '选修课', 20)
    python.add_student(lily)
    java.add_student(rose)
    python.name = 'Python 精讲课'
    python.show_infos()
    java.show_infos()
    
    swift = Course('swift', 3, tom, [jack, lily], '选修课', 20)
    print(Course.show_courseList())
    