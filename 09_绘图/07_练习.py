import turtle as t
import random as r

t.pensize(10)
t.colormode(255)
t.hideturtle()



for i in range(5, 0, -1):
    t.color(
        r.randint(0, 255),
        r.randint(0, 255),
        r.randint(0, 255)
    )
    
    radius = 30 * i
    
    t.penup()
    t.sety(-radius)
    t.pendown()
    
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

t.mainloop()