import turtle as t 
import random as r

t.pensize(10)
t.hideturtle()
t.colormode(255)

for i in range(6, 1, -1):
    t.color(
        r.randint(0, 255),
        r.randint(0, 255),
        r.randint(0, 255)
    )
    # 半径
    radius = i* 30
    t.penup()
    t.sety(-radius)
    t.pendown()
    
    t.begin_fill()
    t.circle(radius)
    t.end_fill()


t.mainloop()
