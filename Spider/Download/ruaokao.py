import subprocess
import os
import threading
import time

speter = '-'*10

# 获取当前脚本所在目录（绝对路径）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_FILE = os.path.join(BASE_DIR, "videos.txt")  # 在同一目录下查找 videos.txt
SAVE_DIR = "/Users/adam/Downloads/XiaoE_Videos"  # 修改为你想存放的目录
os.makedirs(SAVE_DIR, exist_ok=True)  # 若不存在则自动创建
# 统一请求头
COMMON_HEADERS = [
    "--user-agent",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "--add-header",
    "Referer: https://appfdjcorj09314.h5.xiaoeknow.com/",
    "--add-header",
    "Origin: https://appfdjcorj09314.h5.xiaoeknow.com",
    "--concurrent-fragments",
    "8",
]

# 如果你需要 cookies.txt 登录
COOKIES_FILE = "cookies.txt"  # 可选
USE_COOKIES = os.path.exists(COOKIES_FILE)

lock = threading.Lock()


def download_video(title, url, max_retries=2, retry_interval=5):
    """调用 yt-dlp 下载单个视频，失败时自动重试"""
    

    cmd = ["yt-dlp"] + COMMON_HEADERS
    if USE_COOKIES:
        cmd += ["--cookies", COOKIES_FILE]
    # 指定输出路径，保存到 SAVE_DIR 目录
    output_path = os.path.join(SAVE_DIR, f"{title}.%(ext)s")
    cmd += ["-o", output_path, url]

    for attempt in range(1, max_retries + 1):
        print(f"🚀 正在下载：{title}（尝试 {attempt}/{max_retries}）")
        try:
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            print(f"✅ 下载成功：{title}")
            return True
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr if e.stderr else (e.output if e.output else str(e))
            err_msg = err_msg.strip() if err_msg else "未知错误"
            print(f"❌ 下载失败：{title}\n错误信息：{err_msg}")
            if attempt < max_retries:
                print(f"⏳ {retry_interval}秒后重试...")
                time.sleep(retry_interval)
            else:
                print(f"❌ 已重试{max_retries}次仍失败：{title}")
    # 自动清理残留碎片文件
    for filename in os.listdir(SAVE_DIR):
        if ".part-Frag" in filename:
            try:
                os.remove(os.path.join(SAVE_DIR, filename))
            except Exception:
                pass
    print("🧹 已清理下载残留碎片")
    return False



def update_status(lines, index, new_status):
    """更新指定行的状态为 new_status，线程安全"""
    with lock:
        parts = lines[index].strip().split("|")
        if len(parts) < 3:
            # 如果没有状态列，补充状态列
            parts += [""] * (3 - len(parts))
        parts[2] = new_status
        lines[index] = "|".join(parts) + "\n"


def worker(title, url, index, lines):
    if download_video(title, url):
        update_status(lines, index, "done")


def main():
    with open(VIDEOS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if not line.strip() or "|" not in line:
            continue
        parts = line.strip().split("|")
        if len(parts) < 2:
            continue
        title = parts[0].strip()
        url = parts[1].strip()
        status = parts[2].strip() if len(parts) >= 3 else ""

        if status.lower() == "done":
            print(f"⏭ 跳过已完成：{title}")
            continue

        if not url.startswith("http"):
            print(f"❌ 无效URL：{url}")
            continue

        worker(title, url, i, lines)

    # 写回更新后的文件
    with open(VIDEOS_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    
    print(f"{speter*2}Finished{speter*2}")
    try:
        main()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
        # 清理残留碎片
        for filename in os.listdir(SAVE_DIR):
            if ".part-Frag" in filename:
                try:
                    os.remove(os.path.join(SAVE_DIR, filename))
                except Exception:
                    pass
        print("🧹 已清理下载残留碎片")
    finally:
        print(f"{speter*2}Finished{speter*2}")