import turtle as t


t.hideturtle()
t.pencolor('green')
t.pensize(5)
# 填充色
t.fillcolor('red')

# 开始填充
t.begin_fill()



# 第一条边
t.forward(100)

# 第二条边
t.right(90)
t.forward(100)

# 结束填充
t.end_fill()

# 填充色
t.fillcolor('blue')

# 开始填充
t.begin_fill()
# 第3条边
t.right(90)
t.forward(100)

# 第4条边
t.right(90)
t.forward(100)


# 结束填充
t.end_fill()

t.mainloop()