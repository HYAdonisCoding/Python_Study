import turtle as t

# 定义一个画正方形的函数

def draw_square():
    for _ in range(4):
        t.forward(50)
        t.right(90)

def config_point(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    draw_square()
    
t.hideturtle()

# 画第一个正方形
config_point(120, 60)

    
# 画第二个正方形
config_point(-75, 98)

# 画第三个正方形
config_point(-86, -110)

    
# 画第四个正方形
config_point(53, -69)


t.mainloop()