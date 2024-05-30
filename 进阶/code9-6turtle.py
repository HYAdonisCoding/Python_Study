import turtle as t, time
from easy_package import easy_tools

t.penup()
t.backward(200)
# t.mainloop()
while True:
    time.sleep(1)
    times = easy_tools.get_time()
    t.clear()
    t.write(times, font=("Arial", 40, "normal"))
    # print(times)
    
