def hello(name, times, **kwargs):
    for _ in range(times):
        print(f'Hi, {name}!')

d = {
    'name': 'Eason',
    'times': 3,
    'title': 'yyyy'
    }

hello(**d)
hello(name='Mike', times=2, title='yyy')

hello('Eason', 3)