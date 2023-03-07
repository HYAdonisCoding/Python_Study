import turtle as t

# 定义一个画正方形的函数
def draw_square(side):
    for _ in range(4):
        t.forward(side)
        t.right(90)

# 定义一个挪动位置的函数
def move(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    
# 定义一个挪动位置+画正方形的函数
def config_point(x, y, side):
    move(x, y)
    draw_square(side)
    
t.hideturtle()

# 画第一个正方形
config_point(120, 60, 100)
    
# 画第二个正方形
config_point(-75, 98, 80)

# 画第三个正方形
config_point(-86, -110, 50)
    
# 画第四个正方形
config_point(53, -69, 60)


t.mainloop()