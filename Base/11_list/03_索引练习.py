import turtle as t 
import random as r

# 待选颜色
colors =['red', 'blue', 'grey', 'purple', 'orange', 'cyan', 'pink', 'yellow']

t.hideturtle()
t.pensize(10)


for _ in range(4):
    i = r.randrange(len(colors))
    t.color(colors[i])
    t.forward(100)
    t.right(90)

t.mainloop()