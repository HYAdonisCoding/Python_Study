# def say_hello(name):
#     if name:
#         print(f'Hello, {name}!')
#         print(f'您好, {name}!')

def say_hello(name):
    if not name:
        return
    print(f'Hello, {name}!')
    print(f'您好, {name}!')
        
say_hello('Eason')
say_hello('燕云少君')
say_hello('')