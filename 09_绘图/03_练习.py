import turtle as t

t.color('green')
t.shape('square')

t.stamp()

for _ in range(50):
    t.forward(50 + _ * 5)
    t.right(60)
    t.stamp()


t.mainloop()