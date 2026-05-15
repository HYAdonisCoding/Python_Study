import os
import re

# 文件夹路径
folder_path = r"/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/Documents/高项相关/论文2026"
output_file = os.path.join(folder_path, "merged.md")

# 支持的前缀（忽略大小写）
prefixes = ['A', 'B', 'C', 'D']

# 找出符合条件的文件
files = [f for f in os.listdir(folder_path) 
         if any(f.upper().startswith(p) for p in prefixes) and f.endswith('.md')]

# 提取前缀和数字，用于排序
def sort_key(filename):
    match = re.match(r'([A-Da-d])(\d+)_', filename)
    if match:
        prefix, number = match.groups()
        return (prefix.upper(), int(number))
    else:
        return ('Z', 0)  # 不匹配的放后面

# 按前缀和数字排序
files.sort(key=sort_key)

# 合并文件
with open(output_file, 'w', encoding='utf-8') as outfile:
    for i, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            outfile.write(content)
        if i != len(files) - 1:
            outfile.write('\n\n---\n\n')

print(f"已成功合并 {len(files)} 个文件到 {output_file}")