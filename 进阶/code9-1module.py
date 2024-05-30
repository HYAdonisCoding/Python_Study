# import easy_math
# result = easy_math.add(4, 5)
# print(result)
# print(easy_math.auther)

# from easy_package import easy_math
# result = easy_math.add(4, 5)
# print(result)
# print(easy_math.auther)

# from easy_package.easy_math import *
# result = add(4, 5)
# print(result)
# print(auther)

from easy_package.easy_math import add as fun
result = fun(4, 5)
print(result)