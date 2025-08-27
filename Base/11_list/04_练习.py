s = [56 , 78, 100, 89, 0, 96]

if all(s): # 所有分数都不为0
    print('没有0分的学员')
else:
    print('有0分的学员')
    
# 3
# zero = False
# for i in s:
#     if i:
#         continue
#     zero = True
#     break

# if zero: 
#     print('有0分的学员')
# else:
#     print('没有0分的学员')

# 2
# zero = False
# for i in s:
#     if not i:
#         zero = True
#         break

# if zero: 
#     print('有0分的学员')
# else:
#     print('没有0分的学员')
    
# 1
# zero = False
# for i in s:
#     if i == 0:
#         zero = True
#         break

# if zero: 
#     print('有0分的学员')
# else:
#     print('没有0分的学员')