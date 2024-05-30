import random, re, time


def random_string(length):
    s = ''
    for i in range(length):
        s = s + random_char(random.randint(0, 3))
        
    return s

def random_char(type=1):
    if type==1:
        c = random.randint(ord('A'), ord('Z'))
        return chr(c)
    elif type==2:
        c = random.randint(ord('a'), ord('z'))
        return chr(c)
    else:
        c = random.randint(ord('0'), ord('9'))
        return chr(c)

def verify_phone_number(phone):
    r = re.match(r'^1[3-9]\d{9}$', phone)
    return bool(r)
def verify_id_number(phone):
    '''前6位是地区码（前两位为省级行政区划代码，第三到第六位为地级行政区划代码）。
接下来8位是生日信息，前四位为年份，中间两位为月份，最后两位为日期。
倒数第二位是性别标识位，奇数为男性，偶数为女性。
最后一位是校验位，用于校验身份证号码的合法性。'''
    r = re.match(r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[01])\d{3}[\dX]$', phone)
    return bool(r)

def get_time(style='%Y-%m-%d %H:%M:%S'):
    s = time.strftime(style)
    return s
if __name__ == '__main__':
    print(random_string(5))
    print(verify_phone_number('1820315644'))
    print(verify_id_number('110228199902294567'))
    print(get_time())
    print(get_time('%Y-%m-%d'))
    print(get_time('%H:%M:%S'))