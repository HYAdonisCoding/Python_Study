import turtle as t

# side = (int(input('请输入正方形的边长： ')))
# side = (int(t.textinput('请输入', '正方形的边长： ')))
side = (t.numinput('请输入', '正方形的边长： '))

for i in range(4):
    t.forward(side)
    t.right(90)

t.mainloop()
