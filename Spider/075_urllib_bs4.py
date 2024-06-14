import os
from bs4 import BeautifulSoup

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'

def get_data():
    soup = BeautifulSoup(open(current_directory+'075_urllib_bs4.html', 'r', encoding='utf-8'), 'lxml')
    
    # Get the name 
    name_list = soup.select('div strong')
    
    for name in name_list:
        print(name.get_text())
        
if __name__ == '__main__':
    get_data()