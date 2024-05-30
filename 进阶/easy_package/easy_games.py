import random

# 石头剪刀布
def rockPaperScissors():
    player_score, computer_score= 0, 0
    for i in range(3):
        p = input("请输入石头剪刀布：")
        c = random.choice(['石头', '剪刀', '布'])
        print(f'选手出的是：{p}, 电脑出的是：{c}')
        if p == c:
            pass
        elif (p == '石头' and c == '剪刀') or \
            (p == '剪刀' and c == '布') or\
            (p == '布' and c == '石头'):
            player_score += 1
        else:
            computer_score += 1
    print(f'选手得分是：{player_score}, 电脑得分是：{computer_score}')
    if player_score == computer_score:
        print(f'平局了')
    elif player_score > computer_score:
        print(f'玩家胜利')
    else:
        print(f'电脑胜利')


def guess_number(start, end):
    number = random.randint(start, end)
    while True:
        player = int(input('请输入您猜的数字：'))
        if player == number:
            print('Congratulations, you guessed it right')
            break
        elif player > number:
            print('Guess it\'s too big')
        else:
            print('Guess it\'s too small')
            
if __name__ == '__main__':
    guess_number(0, 100)