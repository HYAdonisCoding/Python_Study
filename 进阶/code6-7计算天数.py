# 题目要求：输入2024-05-28，输出这一天是这一年的多少天

date = input('请输入日期：').split('-')

year, month, day = int(date[0]), int(date[1]), int(date[2])

print(year, month, day)
# 判断是否是闰年
is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

days = [0, 31, 28+is_leap_year, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,]

result = 0
for i in range(month):
    result += days[i]
result += day
print('%d-%02d-%02d是%d年的第%d天' % (year, month,day, year, result))
