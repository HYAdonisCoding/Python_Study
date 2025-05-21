import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os

def download_image(url, save_path):
    """
    下载图片的函数
    :param url: 图片的 URL
    :param save_path: 图片保存的路径
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"图片下载成功: {save_path}")
    except requests.RequestException as e:
        print(f"下载图片时出错: {e}")

def get_weibo_images(weibo_url, save_folder):
    """
    获取微博图片并下载的函数
    :param weibo_url: 微博的 URL
    :param save_folder: 图片保存的文件夹
    """
    # 创建保存图片的文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 创建 Chrome 浏览器实例
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)# 保持打开
    driver = webdriver.Chrome(options=options)
    try:
        # 打开微博页面
        driver.get(weibo_url)
        # 等待页面加载
        time.sleep(5)

        # 查找所有图片元素
        img_elements = driver.find_elements(By.CSS_SELECTOR, 'img')
        for index, img in enumerate(img_elements):
            # 获取图片的 src 属性
            img_url = img.get_attribute('src')
            if img_url:
                # 处理图片 URL 以获取高清大图
                if 'thumb150' in img_url:
                    img_url = img_url.replace('thumb150', 'large')
                # 生成图片保存的文件名
                file_name = os.path.join(save_folder, f'image_{index}.jpg')
                # 下载图片
                download_image(img_url, file_name)
    except Exception as e:
        print(f"出现错误: {e}")
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    # 替换为你要爬取的微博 URL
    weibo_url = 'https://www.weibo.com/u/6217939256'
    # 替换为你要保存图片的文件夹路径
    save_folder = 'weibo_images'
    get_weibo_images(weibo_url, save_folder)