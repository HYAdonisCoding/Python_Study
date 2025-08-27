import turtle as t
import random as r

t.pensize(20)
t.hideturtle()
t.colormode(255)

# 第一条边
t.pencolor(
    r.randint(0, 255),
    r.randint(0, 255),
    r.randint(0, 255)
)
t.forward(100)

# 第二条边
t.pencolor(
    r.randint(0, 255),
    r.randint(0, 255),
    r.randint(0, 255)
)
t.right(90)
t.forward(100)

# 第三条边
t.pencolor(
    r.randint(0, 255),
    r.randint(0, 255),
    r.randint(0, 255)
)
t.right(90)
t.forward(100)

# 第四条边
t.pencolor(
    r.randint(0, 255),
    r.randint(0, 255),
    r.randint(0, 255)
)
t.right(90)
t.forward(100)

t.mainloop()