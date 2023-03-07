import turtle as t

# 挪动位置+画圆
def move_circle(*, x, y, radius):
    t.penup()
    t.goto(x, y)
    t.pendown()
    
    t.circle(radius)

# 等价于move_circle(100, 0, 50)
move_circle(x=50, y=60, radius=70)
# s = [-10, -50, 70]
# move_circle(*s)

t.mainloop()