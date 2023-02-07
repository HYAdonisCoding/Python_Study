import turtle as t
import random as r

colors = ['red', 'blue', 'green', 'gray', 'purple', 'orange', 'cyan', 'pink']

t.hideturtle()
t.pensize(10)

t.begin_fill()

for _ in range(4):
    i = r.randrange(len(colors))
    t.pencolor(colors.pop(i))
    
    t.forward(100)
    t.right(90)

t.fillcolor(colors[r.randrange(len(colors))])
t.end_fill()

t.mainloop()