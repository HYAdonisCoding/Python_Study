import turtle as t

t.hideturtle()

radius = 150
x = -30

# 右半圆
t.circle(radius, 180)
t.goto(0, 0)

# 
t.penup()
t.goto(x, 0)
t.pendown()


t.circle(-radius, 180)
t.goto(x, 0)

t.mainloop()