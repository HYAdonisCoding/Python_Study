import turtle as t 

t.color('green')
# 设置方向箭头的图案
t.shape('turtle')

# 盖章
t.stamp()

for _ in range(50):
    t.forward(50 + _ * 5)
    t.right(60)
    t.stamp()


t.mainloop()
