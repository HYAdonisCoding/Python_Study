# # 用户名、密码、黑名单
# users = [
#     {'name': '小红','password': '123', 'status': True},
#     {'name': 'Jay','password': '345', 'status': True},
#     {'name': 'Jack','password': '678', 'status': False},
# ]

# print(users)

# flag = False
# for j in range(3):
#     user = input('Enter your username:')
#     pwd = input('Enter your password:')
#     for i in users:
#         if i['name'] == user:
#             if i['password'] == pwd:
#                 if i['status'] == True:
#                     print('login successful')
#                     flag = True
#                     break
#                 else:
#                     print('login failed, please try again')
#             else:
#                 print('login failed, password is incorrect')
#             break
#     else:
#         print('login failed please register' )
#     if flag:
#         break

# 用户名、密码、黑名单
users = {
    '小红': {'name': '小红','password': '123', 'status': True},
    'Jay': {'name': 'Jay','password': '345', 'status': True},
    'Jack': {'name': 'Jack','password': '678', 'status': False},
}

print(users)

for j in range(3):
    user = input('Enter your username:')
    pwd = input('Enter your password:')
   
    if user in users and users[user]['password'] == pwd and users[user]['status']:
        print('login successful！！！')
        break
    elif user in users and not users[user]['status']:
       print('login failed, please contact the administrator!')
    elif user in users and pwd != users[user]['password']:
        print('login failed, password is incorrect!')
            
    else:
        print('login failed please register first!' )
