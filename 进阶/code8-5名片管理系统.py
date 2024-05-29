cards = [{'name': 'Mike', 'phone': '13901234567', 'qq': '789456', 'email': 'sfhf.qq.com'},
         {'name': 'Jack', 'phone': '13901123456', 'qq': '7894571', 'email': 'dsdwfw.qq.com'},
         {'name': 'Eason', 'phone': '1390101120', 'qq': '45634313', 'email': 'sdfsdf.qq.com'}]

def menu():
    print('*' * 30)
    print('''欢迎使用【名片管理系统】
          1.新建名片
          2.显示全部
          3.查询名片
          0.退出系统
          ''')
    print('*' * 30)
    
def new_card(name, phone, qq, email):
    cards.append({'name': name, 'phone': phone, 'qq': qq, 'email': email})
    return True

def modify_card(card, idx, content):
    if idx == '6':
        card['name'] = content
    elif idx == '7':
        card['phone'] = content
    elif idx == '8':
        card['qq'] = content
    elif idx == '9':
        card['email'] = content

def delete_card(card):
    cards.remove(card)

def show_cards():
    for card in cards:
        print(card)
def query_card(kw):
    for card in cards:
        for k, v in card.items():
            if kw==v:
                return card
    return False

def quite():
    print('*' * 30)
    print('欢迎下次使用【名片管理系统】再见')
    print('*' * 30)
    
menu()

while True:
    op = input('请输入您要的操作序号：')
    if op=='1':
        name = input('请输入您的姓名：')
        phone = input('请输入您的手机号：')
        qq = input('请输入您的QQ号：')
        email = input('请输入您电子邮箱：')

        result = new_card(name, phone, qq, email)
        if result:
            print('Created new card successfully')
        else:
            print('New card failed, please try again')
    elif op=='2':
        show_cards()
    elif op=='3':
        kw = input('请输入查询的关键字：')
        result = query_card(kw)
        if result:
            print('Query card successfully')
            print(result)
            
            o = input('输入4修改名片，输入5删除名片：')
            if o == '4':
                print('''请输入修改的项目：
                    6.修改姓名
                    7.修改电话
                    8.修改QQ
                    9.修改Email
                    ''')
                idx = input('输入要修改的序号：')
                content = input('输入要修改的内容：')
                modify_card(result, idx, content)
                print('Modified card successfully')
            elif o == '5':
                delete_card(result)
                print('Delete card successfully')
        else:
            print('Query card failed')
    elif op=='0':
        quite()
        break
    else:
        print('Please try again!')