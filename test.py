import turtle as t

def draw_01():
    for i in range(50):
        t.forward(i * 5)
        t.right(90)

    t.mainloop()

def draw_02():
    t.color('green')
    t.shape('turtle')
    t.stamp()

    for i in range(50):
        t.forward(50 + i * 5)
        t.right(60)
        t.stamp()
    t.mainloop()

def draw_03():
    t.color('pink')
    t.pensize(30)
    t.begin_fill()
    t.left(50)
    t.circle(-100, 180)
    t.right(10)
    t.forward(200)
    t.right(80)
    t.forward(200)
    t.right(10)
    t.circle(-100, 180)
    t.end_fill()
    
    t.mainloop()

def draw_04():
    t.color('pink')
    t.pensize(30)
    t.begin_fill()
    t.left(50)
    t.circle(-100, 180)
    t.right(10)
    t.forward(200)
    t.right(80)
    t.forward(200)
    t.right(10)
    t.circle(-100, 180)
    t.end_fill()
    
    t.hideturtle()
    t.color('red')
    t.pensize(8)
    t.penup()
    t.goto(-7, 22)
    t.pendown()
    dis = 25
    t.forward(dis)
    angle = 80
    for i in range(7):
        t.right(angle)
        t.forward(dis)
        t.left(angle)
        t.forward(dis)
    t.mainloop()

draw_04()