# -*- coding: utf-8 -*-
import ssl
import urllib.request
import os
import certifi

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'


print("当前文件目录:", current_directory)

def main():
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    }
    # 下载网页
    # url_page = 'http://www.google.com'
    # file = current_directory + 'google.html'
    # urllib.request.urlretrieve(url_page, file)
    
    # 下载图片
    # url_image = 'https://n.sinaimg.cn/default/4_img/upload/3933d981/100/w1000h1500/20180914/RI5W-hhuhism0630680.jpg'
    # image_file = current_directory + 'girl.jpg'
    # # 使用 urlretrieve 下载文件
    # urllib.request.urlretrieve(url_image, image_file)
    
    # download video
    url_video = 'https://vd3.bdstatic.com/mda-pk0ed3nnye3bcnih/sc/cae_h264/1698848022121465276/mda-pk0ed3nnye3bcnih.mp4?v_from_s=hkapp-haokan-hbe&auth_key=1704455649-0-0-e0be38a683dbfb161c309c4e1c210dbe&bcevod_channel=searchbox_feed&pd=1&cr=2&cd=0&pt=3&logid=3249020457&vid=5712386337347028874&klogid=3249020457&abtest='
    video_file = current_directory + 'hot.mp4'
    # 使用 urlretrieve 下载文件
    urllib.request.urlretrieve(url_video, video_file)
    
    print('Hello, World!')

if __name__ == '__main__':
    main() 