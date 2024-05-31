import csv, os, random
from easy_package import easy_tools
# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 打开文件
filename = script_dir + '/data.csv'
# list_array = [['name', 'subject', 'score'],['Eason', 'Python', '90'],['Eason', 'Swift', '80'],['Eason', 'Java', '80']]
list_array = []

def random_data(n=10):
    subjects = ['Object-C', 'Java', 'Python', 'Html', 'Swift', 'SwiftUI', 'C', 'JS']
    names = []
    for i in range(n//len(subjects)):
        name = easy_tools.generate_random_name()
        names.append(name)
        
    for i in range(n):
        subject = random.choice(subjects)
        score = random.randint(50, 100)
        name = random.choice(names)
        for j in list_array:
            if j[0] == name and j[1] == subject:
                break
        else:
            list_array.append([name, subject, score])
    print (list_array)

def make_datas():
    with open(filename, 'a') as f:
        cf = csv.writer(f)
        random_data(100)
        cf.writerows(list_array)

def average_score():
    with open(filename, 'r') as f:
        cf = csv.reader(f)
        header = next(cf) # 获取标头
        scores = []
        for i in cf:
            scores.append(int(i[2]))
        return sum(scores)/len(scores)
            
from collections import defaultdict

def calculate_scores(filename):
    # 初始化数据结构
    student_scores = defaultdict(list)
    subject_scores = defaultdict(list)
    
    # 初始化最高分数据结构
    subject_max_scores = defaultdict(lambda: {"score": 0, "students": []})
    
    # 读取CSV文件并填充数据结构
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # 跳过表头
        for row in reader:
            name, subject, score = row
            score = int(score)
            student_scores[name].append(score)
            subject_scores[subject].append(score)
            
            # 检查并更新每科最高分
            if score > subject_max_scores[subject]["score"]:
                subject_max_scores[subject] = {"score": score, "students": [name]}
            elif score == subject_max_scores[subject]["score"]:
                subject_max_scores[subject]["students"].append(name)
    
    
    # 计算每个人的平均分和最高分
    student_averages = {name: sum(scores) / len(scores) for name, scores in student_scores.items()}
    student_max_scores = {name: max(scores) for name, scores in student_scores.items()}
    
    # 计算每科的平均分
    subject_averages = {subject: sum(scores) / len(scores) for subject, scores in subject_scores.items()}
    
    # 对每个人的平均分和最高分进行排序
    sorted_student_averages = sorted(student_averages.items(), key=lambda x: x[1], reverse=True)
    sorted_student_max_scores = sorted(student_max_scores.items(), key=lambda x: x[1], reverse=True)
    
    # 对每科的平均分进行排序
    sorted_subject_averages = sorted(subject_averages.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_student_averages, sorted_student_max_scores, sorted_subject_averages, subject_max_scores

if __name__ == '__main__':
    # make_datas()
    # c = average_score()
    # print(f'Average score is: {round(c,2)}')
    
    
    # 使用
    sorted_student_averages, sorted_student_max_scores, sorted_subject_averages, subject_max_scores = calculate_scores(filename)


    print("每个人的平均分（按平均分排序）:")
    for student, avg in sorted_student_averages:
        print(f"{student}: {avg:.2f}")

    print("\n每个人的最高分（按最高分排序）:")
    for student, max_score in sorted_student_max_scores:
        print(f"{student}: {max_score}")

    print("\n每科的平均分（按平均分排序）:")
    for subject, avg in sorted_subject_averages:
        print(f"{subject}: {avg:.2f}")

    print("\n每科的最高分及其对应的学生:")
    for subject, data in subject_max_scores.items():
        students = ', '.join(data["students"])
        print(f"{subject}: {data['score']} (Students: {students})")
    pass