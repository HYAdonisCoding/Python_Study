# -*- coding: utf-8 -*-

import ssl

import certifi
import urllib.request
import urllib.error


def main():
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)

    url = 'https://blog.csdn.net/qq_57761637/article/details/135098775?spm=1001.2100.3001.7377&utm_medium=distribute.pc_feed_blog_category.none-task-blog-classify_tag-3-135098775-null-null.nonecase&depth_1-utm_source=distribute.pc_feed_blog_category.none-task-blog-classify_tag-3-135098775-null-null.nonecase'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        # 1.请求对象的定制
        request = urllib.request.Request(url=url, headers=headers)
        # 2.获取想要的数据
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        # 3.数据下载到本地
        # open默认gbk编码
        # fp = open(current_directory+'douban1.json', 'w', encoding='utf-8')
        # fp.write(content)
        print(content)
    except urllib.error.HTTPError as e:
        print('系统正在升级...', e)
    except urllib.error.URLError as e:
        print('系统正在升级中...', e)
if __name__ == '__main__':
    main()