import turtle as t 
import random as r

t.pensize(10)
t.hideturtle()
t.colormode(255)

for i in range(1, 6):
    t.pencolor(
        r.randint(0, 255),
        r.randint(0, 255),
        r.randint(0, 255)
    )
    # 半径
    radius = i* 30
    t.penup()
    t.sety(-radius)
    t.pendown()
    t.circle(radius)


t.mainloop()
