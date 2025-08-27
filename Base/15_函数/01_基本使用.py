import turtle as t

t.hideturtle()

# 画第一个正方形
t.penup()
t.goto(120, 60)
t.pendown()
for _ in range(4):
    t.forward(50)
    t.right(90)
    
# 画第二个正方形
t.penup()
t.goto(-75, 98)
t.pendown()
for _ in range(4):
    t.forward(50)
    t.right(90)
    
# 画第三个正方形
t.penup()
t.goto(-86, -110)
t.pendown()
for _ in range(4):
    t.forward(50)
    t.right(90)
    
# 画第四个正方形
t.penup()
t.goto(53, -69)
t.pendown()
for _ in range(4):
    t.forward(50)
    t.right(90)

t.mainloop()