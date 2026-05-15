# -*- coding: utf-8 -*-

import json
import os
import random
import re
from fake_useragent import UserAgent
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getUA():
    uaList = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    ]
    User_Agent = random.choice(uaList)
    return User_Agent


def get_headers():
    ua = UserAgent().random
    headers = {
        "User-Agent": ua if ua else getUA(),
        "Referer": "https://www.listennotes.com/",
    }
    return headers


def download_mp3():
    url = "https://m10.music.126.net/20240703095220/81526e2dbb55fce1c6447c62ee099fcf/yyaac/obj/wonDkMOGw6XDiTHCmMOi/3945547514/6c7d/4fb4/2def/e560cfe0e71e462bec4ef8efcdfadb5c.m4a"
    url = "https://m704.music.126.net/20240703113450/2934cb24662cf52001f84e93f61cee1a/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/17266711921/1541/393f/f4ff/86d26c68acbc6e8c02892334ce8b2274.m4a?authSecret=000001907691e07002170a3b1db51782"
    res = requests.get(url, headers=get_headers(), verify=False, timeout=15)
    with open("诛仙我回来-任贤齐.mp3", "wb") as f:
        f.write(res.content)


# 函数：下载文件
import os
import re
import requests
from enum import Enum


# 定义支持的文件扩展名
class FileExtension(Enum):
    MP3 = ".mp3"
    MP4 = ".mp4"
    M4A = ".m4a"


# 定义下载函数
def download_file(url, filename, default_extension=FileExtension.MP3):
    try:

        # 1. 首先去除系统非法字符
        sanitized_filename = re.sub(r'[\\/*?:"<>|]', "", filename)

        # 2. 判断是否包含中文字符
        # 如果包含中文，则执行去除空格的操作
        if re.search(r"[\u4e00-\u9fa5]", sanitized_filename):
            sanitized_filename = sanitized_filename.replace(" ", "")

        # 检查并自动添加扩展名
        ext = os.path.splitext(sanitized_filename)[1].lower()  # 提取扩展名
        if ext not in [e.value for e in FileExtension]:
            # 如果没有有效扩展名，添加默认扩展名
            sanitized_filename += default_extension.value

        # 下载文件
        response = requests.get(
            url, stream=True, timeout=15, headers=get_headers(), verify=False
        )
        response.raise_for_status()  # 如果状态码不是 2xx，抛出异常

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(sanitized_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

        # 校验文件完整性
        if total_size != 0 and downloaded != total_size:
            print(f"❌ 文件下载不完整: {sanitized_filename}")
            print(f"期望: {total_size} 字节, 实际: {downloaded} 字节")
        else:
            print(f"✅ 下载完成: {sanitized_filename} ({downloaded/1024/1024:.2f} MB)")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")
    except Exception as e:
        print(f"Unknown error occurred for {filename}: {e}")

def download_file_range_continue(url, filename, save_dir=".", default_extension=FileExtension.MP3):
    headers = get_headers()

    filename = re.sub(r'[\\/*?:"<>|]', '', filename)

    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        filename += default_extension.value

    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, filename)
    temp_file = file_path + ".part"

    downloaded = 0
    if os.path.exists(temp_file):
        downloaded = os.path.getsize(temp_file)

    headers["Range"] = f"bytes={downloaded}-"

    try:
        with requests.get(url, headers=headers, stream=True, timeout=(10, 60)) as r:
            r.raise_for_status()

            # ⚠️ Range 失效处理
            if r.status_code == 200 and downloaded > 0:
                print("⚠️ 不支持断点续传，重新下载")
                downloaded = 0

            total_size = int(r.headers.get("content-length", 0)) + downloaded
            print(f"📦 {filename} 总大小: {total_size / 1024 / 1024:.2f} MB")

            mode = "ab" if downloaded > 0 else "wb"

            with open(temp_file, mode) as f:
                for chunk in r.iter_content(chunk_size=1024 * 64):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

        # ✅ 完整性校验
        if total_size != 0 and downloaded != total_size:
            print("❌ 下载不完整")
            return

        os.rename(temp_file, file_path)

        print(f"✅ 下载完成: {file_path}")

    except Exception as e:
        print(f"⚠️ 下载中断: {e}")
        print(f"👉 已保存进度: {downloaded} 字节")


def download_mp4():
    url = "https://vodkgeyttp8.vod.126.net/cloudmusic/NTA5MTI0OTQ=/a7a08ad10ff1fb471e1deaf0c39d1c6f/a687d1e8d5b8666442e3a838aae044a8.mp4?wsSecret=07339ea812d0917da488ee99f8c8f854&wsTime=1719971177"
    res = requests.get(url, headers=get_headers(), verify=False, timeout=15)
    with open("诛仙我回来-任贤齐.mp4", "wb") as f:
        f.write(res.content)


text = """
0:00:00  -- 腾飞五千年之两晋南北朝第01集 双重人格司马炎

0:20:06  -- 腾飞五千年之两晋南北朝第02集 丑人多作怪

0:39:12  -- 腾飞五千年之两晋南北朝第03集 乱世皆可称王

1:01:20  -- 腾飞五千年之两晋南北朝第04集 五胡乱华的起点

1:18:22  -- 腾飞五千年之两晋南北朝第05集 洛阳的陷落

1:37:50  -- 腾飞五千年之两晋南北朝第06集 王与马共天下

1:58:00  -- 腾飞五千年之两晋南北朝第07集 平定王敦之乱

2:17:17  -- 腾飞五千年之两晋南北朝第08集 奴隶奴隶一统北方

2:37:07  -- 腾飞五千年之两晋南北朝第09集 吞不下的肥肉

2:57:11  -- 腾飞五千年之两晋南北朝第10集 冉魏的诞生

3:15:22  -- 腾飞五千年之两晋南北朝第11集 北方二雄主

3:37:15  -- 腾飞五千年之两晋南北朝第12集 被排挤的燕国神将

3:56:56  -- 腾飞五千年之两晋南北朝第13集 前秦一统北方

4:16:22  -- 腾飞五千年之两晋南北朝第14集 不战而败的淝水之战

4:39:25  -- 腾飞五千年之两晋南北朝第15集 北方的乱局魔咒

4:58:30  -- 腾飞五千年之两晋南北朝第16集后燕的崩溃

5:20:19  -- 腾飞五千年之两晋南北朝第17集 凉州四分五裂

5:42:21  -- 腾飞五千年之两晋南北朝第18集 玄桓的皇帝梦

6:03:58  -- 腾飞五千年之两晋南北朝第19集 南北朝的开端

6:24:00  -- 腾飞五千年之两晋南北朝第20集 少年英雄拓跋焘

6:40:48  -- 腾飞五千年之两晋南北朝第21集 北方的新主人

6:57:47  -- 腾飞五千年之两晋南北朝第22集 一言不合 南北开战

7:16:23  -- 腾飞五千年之两晋南北朝第23集 变态皇帝接二连三

7:35:12  -- 腾飞五千年之两晋南北朝第24集 魏孝文帝背后的女人

7:56:37  -- 腾飞五千年之两晋南北朝第25集 同出一脉以梁代齐

8:13:55  -- 腾飞五千年之两晋南北朝第26集 北方帝国的衰败

8:32:27  -- 腾飞五千年之两晋南北朝第27集 侯景乱梁 江南陷落

8:50:39  -- 腾飞五千年之两晋南北朝第28集 南梁变南陈

9:08:32  -- 腾飞五千年之两晋南北朝第29集 北周权臣宇文护

9:29:06  -- 腾飞五千年之两晋南北朝第30集 周武帝伐齐

9:52:50  -- 腾飞五千年之两晋南北朝第31集 杨坚代周自立
"""
import re
import subprocess


# 切分文件
def file_slicing(input_file, output_dir):
    
    os.makedirs(output_dir, exist_ok=True)
    pattern = r"(\d+:\d{2}:\d{2})\s+--\s+(.*)"

    matches = re.findall(pattern, text)

    def format_time(t):
        parts = t.split(":")
        if len(parts[0]) == 1:
            return "0" + t
        return t

    for i in range(len(matches)):
        start_time = format_time(matches[i][0])
        title = matches[i][1].strip()
        title = re.sub(r'[\\/*?:"<>|]', "", title)[:50]

        if i < len(matches) - 1:
            end_time = format_time(matches[i + 1][0])
        else:
            end_time = None

        output = os.path.join(output_dir, f"{i+1:02d}_{title}.m4a")

        if end_time:
            cmd = [
                "ffmpeg",
                "-y",
                "-ss",
                start_time,
                "-to",
                end_time,
                "-i",
                input_file,
                "-c",
                "copy",
                "-avoid_negative_ts",
                "1",
                output,
            ]
        else:
            cmd = [
                "ffmpeg",
                "-y",
                "-ss",
                start_time,
                "-i",
                input_file,
                "-c",
                "copy",
                "-avoid_negative_ts",
                "1",
                output,
            ]

        print(f"正在切割：{i+1}/{len(matches)} - {title}")
        result = subprocess.run(cmd)

        need_reencode = False

        # 1. 如果命令失败
        if result.returncode != 0:
            need_reencode = True

        # 2. 如果输出文件不存在或为0KB（你当前主要问题）
        if not os.path.exists(output) or os.path.getsize(output) == 0:
            need_reencode = True

        if need_reencode:
            print(f"⚠️ copy失败或空文件，强制重编码: {title}")

            if end_time:
                cmd_reencode = [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    start_time,
                    "-to",
                    end_time,
                    "-i",
                    input_file,
                    "-vn",
                    "-acodec",
                    "aac",
                    "-b:a",
                    "128k",
                    "-fflags",
                    "+genpts",
                    "-err_detect",
                    "ignore_err",
                    output,
                ]
            else:
                cmd_reencode = [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    start_time,
                    "-i",
                    input_file,
                    "-vn",
                    "-acodec",
                    "aac",
                    "-b:a",
                    "128k",
                    "-fflags",
                    "+genpts",
                    "-err_detect",
                    "ignore_err",
                    output,
                ]

            subprocess.run(cmd_reencode)

            # 再次校验
            if not os.path.exists(output) or os.path.getsize(output) == 0:
                print(f"❌ 最终仍失败: {title}")


if __name__ == "__main__":
    # download_mp3()
    # headers = get_headers()
    # download_mp4()
    # url = 'https://m804.music.126.net/20240703113706/367059ade90c59363d993c850c07a4db/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/12360274338/3350/04dc/06d2/43db43480ec8778ccf618f492a0cf856.m4a?authSecret=000001907693f45807130a3b192fbfde'
    # filename =  '北京雨燕.mp3'

    # QQ音乐
    # 数据数组
    data_array = [
        {
            "url": "https://m704.music.126.net/20260322154950/06883e102cdb02f7d4888d2429126632/jdyyaac/0f08/5559/0353/8b47c6883fb31070a47949d0e3a9ed6f.m4a?vuutv=o8HjH1MpbNLo1KPTOzzBytvLRh7CYYeQgC/cLNBQzd080Coe5BF3EeS3Xj+bD3t+lIRFdaXnClMqonyqDv7FDB3VtX/gKrYQ9MphcRyAaG8=&authSecret=0000019d146ead1c11840a3b22c012bc&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g",
            "filename": "风居住的街道",
        },
        {
            "url": "https://m804.music.126.net/20260322155154/7c0f14b2bcf45aba32ad2d0e3690d6a9/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/14096443535/a3f0/1d0e/1023/609a9e39e0af8634dc72b1ef4d12e37e.m4a?vuutv=7A3T8ZDZfgf4HPQC6ow3h2DP1k5WoLMOEMjY9ijVaqY0AZryuYkHCVu6xnvEXpyePOOtCxOdgC8MQhYy6wY0QfdwVQNJ/U+6+ds9daDAAWQ=&authSecret=0000019d1470904015dd0a3b1bab050a&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g",
            "filename": "平凡之路",
        },
    ]

    # 遍历数组并下载文件
    for item in data_array:
        download_file_range_continue(
            item["url"], item["filename"], save_dir="/Users/adam/Music", default_extension=FileExtension.MP3
        )
    # for item in data_array:
    #     download_file_range_continue(
    #         item["url"], item["filename"], save_dir="/Volumes/SeagateW/History", default_extension=FileExtension.M4A
    #     )
    print("All Download successfully")
    # print('Start Slicing')
    # input_file = "/Volumes/SeagateW/History/两晋南北朝.m4a"
    # output_dir = os.path.join(os.path.dirname(input_file), "两晋南北朝")
    # file_slicing(input_file, output_dir)
    print('All slicing successfully')
