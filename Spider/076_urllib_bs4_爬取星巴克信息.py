import urllib.request
from bs4 import BeautifulSoup

def get_data():
    url = 'https://www.starbucks.com.cn/menu/'
    url = 'https://www.starbucks.com.cn/coffee-blog'
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    soup = BeautifulSoup(content, 'lxml')
    
    # Get the name //*[@id="content"]/div/ul//h3[@class="blog-related-title"]
    name_list = soup.select('div ul h3[class="blog-related-title"]')
    
    for name in name_list:
        print(name.get_text())
        
if __name__ == '__main__':
    get_data()