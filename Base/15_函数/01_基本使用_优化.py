import turtle as t

# 定义一个画正方形的函数

def draw_square():
    for _ in range(4):
        t.forward(50)
        t.right(90)

t.hideturtle()

# 画第一个正方形
t.penup()
t.goto(120, 60)
t.pendown()
draw_square()
    
# 画第二个正方形
t.penup()
t.goto(-75, 98)
t.pendown()
draw_square()

# 画第三个正方形
t.penup()
t.goto(-86, -110)
t.pendown()
draw_square()
    
# 画第四个正方形
t.penup()
t.goto(53, -69)
t.pendown()
draw_square()

t.mainloop()