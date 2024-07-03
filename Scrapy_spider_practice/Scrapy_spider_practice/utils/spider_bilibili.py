import os
import requests
import spider_163
import subprocess

def download_video(video_url, output_path, cookies_file):
    command = [
        'youtube-dl',
        '-f', 'best',
        '-o', output_path,
        '--cookies', cookies_file,
        '--add-header', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        '--add-header', 'Referer: https://www.bilibili.com/video/BV1tE4m1R7AL',
        video_url
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return None, None
def download_video_yl(video_url, output_path, cookies_file):
    command = [
        'yt-dlp',
        # '-f', 'best',
        '-o', output_path,
        '--cookies', cookies_file,
        '--add-header', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        '--add-header', 'Referer: https://www.bilibili.com/video/BV1tE4m1R7AL',
        video_url
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return None, None
def download_mp4():
    # url = 'https://api.bilibili.com/x/player/online/total?aid=1256231402&cid=1602638009&bvid=BV1tE4m1R7AL&ts=57332397'
    # url = 'https://api.bilibili.com/x/player/online/total?aid=1256231402&cid=1602638009&bvid=BV1tE4m1R7AL&ts=57332395'
    # p_url = 'https://data.bilibili.com/v2/log/web?content_type=pbrequest&logid=021434&disable_compression=true'
    headers=spider_163.get_headers()
    headers['Referer'] = 'https://www.bilibili.com/video/BV1tE4m1R7AL/?t=6&spm_id_from=333.1007.tianma.1-2-2.click'
    
    # res = requests.get(url, headers=headers)
    # # res1 = requests.post(p_url, headers=spider_163.get_headers())
    # with open('b站.mp4', 'wb') as f:
    #     f.write(res.content)
    # 视频URL和输出文件路径
    video_url = 'https://www.bilibili.com/video/BV1tE4m1R7AL'
    output_path = 'b站.mp4'
    # 获取当前文件所在目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    cookies_file = current_directory +'/bilibili_cookies.txt'
    headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer: https://www.bilibili.com/video/BV1tE4m1R7AL/?t=6&spm_id_from=333.1007.tianma.1-2-2.click"
    ]
    # 下载视频并捕获输出
    stdout, stderr = download_video_yl(video_url, output_path, cookies_file)

    if stdout or stderr:
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
    else:
        print("Failed to download the video.")
if __name__ == '__main__':
    # download_mp3()
    # headers = get_headers()
    # ffmpeg -i "https://www.bilibili.com/video/BV1tE4m1R7AL" -c copy video.mp4
    download_mp4()
    print('download successfully')
