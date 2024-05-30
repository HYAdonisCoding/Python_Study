import re 

# 数字：\d
result = re.match(r'\d+', '123')
print(result)


# 数字字母下划线：\w
result = re.match(r'^\w+$', '1213_w!')
print(result)

# 空白字符：\s, 非空字符\S
result = re.match(r'^\s+', '   q')
print(result)

# 任意字符：.
result = re.match(r'^code\d+-\d.+\.py$', 'code9-4re.py')
print(result)

# 区间、可选列表：[]
result = re.match(r'^[A-Z]+$', 'ASE')
print(result)

# 或者：|
result = re.match(r'^S|Z+$', 'SSEZ')
print(result)

# 匹配到前面的n到m次前面的正则表达式：{n, m}
result = re.match(r'^abc{2,5}$', 'abccccc')
print(result)


from easy_package import easy_tools

# 身份证号码
print(easy_tools.verify_id_number('110228191002304658'))
# 手机号码
print(easy_tools.verify_phone_number('13901234567'))