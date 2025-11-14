#!/usr/bin/env python3
import os
import shutil

# 缓存目录列表
paths = {
    "Xcode DerivedData": os.path.expanduser("~/Library/Developer/Xcode/DerivedData"),
    "Xcode Archives": os.path.expanduser("~/Library/Developer/Xcode/Archives"),
    "Xcode DeviceSupport": os.path.expanduser("~/Library/Developer/Xcode/iOS DeviceSupport"),
    "CoreSimulator Devices": os.path.expanduser("~/Library/Developer/CoreSimulator/Devices"),
    "CoreSimulator Caches": os.path.expanduser("~/Library/Developer/CoreSimulator/Caches"),
    "System Cache": os.path.expanduser("~/Library/Caches"),
    "User Logs": os.path.expanduser("~/Library/Logs"),
    "Trash": os.path.expanduser("~/.Trash"),
    "Temp Files": "/tmp",
    "Safari Cache": os.path.expanduser("~/Library/Caches/com.apple.Safari"),
    "Chrome Cache": os.path.expanduser("~/Library/Caches/Google/Chrome"),
    "Firefox Cache": os.path.expanduser("~/Library/Caches/Firefox")
}

def get_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                if os.path.isfile(fp):
                    total += os.path.getsize(fp)
            except Exception:
                pass
    return total

def human_readable(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"

def clean_cache(path):
    if os.path.exists(path):
        for f in os.listdir(path):
            fp = os.path.join(path, f)
            try:
                if os.path.isfile(fp) or os.path.islink(fp):
                    os.unlink(fp)
                elif os.path.isdir(fp):
                    shutil.rmtree(fp)
            except PermissionError:
                print(f"[跳过权限受限]: {fp}")
            except Exception as e:
                print(f"[错误]: {fp} -> {e}")

def main():
    print("📊 缓存目录及大小：")
    for name, path in paths.items():
        if os.path.exists(path):
            print(f"{name}: {human_readable(get_size(path))}")
        else:
            print(f"{name}: Not Found")
    
    confirm = input("⚠️ 是否清理以上缓存目录？(y/n): ")
    if confirm.lower() != 'y':
        print("已取消清理。")
        return

    total_before = sum(get_size(p) for p in paths.values() if os.path.exists(p))
    for name, path in paths.items():
        if os.path.exists(path):
            print(f"清理: {name} ...")
            clean_cache(path)

    total_after = sum(get_size(p) for p in paths.values() if os.path.exists(p))
    released = total_before - total_after
    print(f"\n✅ 清理完成！总共释放: {human_readable(released)}")

if __name__ == "__main__":
    main()