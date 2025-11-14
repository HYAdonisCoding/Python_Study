#!/usr/bin/env python3
import os
import shutil
import subprocess
import glob

THRESHOLD = 1 * 1024 * 1024  # 1 MB

def human_readable(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"

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

def scan_user_caches():
    user_cache_root = os.path.expanduser("~/Library/Caches")
    app_support_root = os.path.expanduser("~/Library/Application Support")
    dirs = []
    
    # 扫描 Caches 根目录
    if os.path.exists(user_cache_root):
        for sub in os.listdir(user_cache_root):
            path = os.path.join(user_cache_root, sub)
            if os.path.isdir(path):
                dirs.append((get_size(path), path))

    # 扫描 Application Support 下 Cache/Local
    if os.path.exists(app_support_root):
        for sub in os.listdir(app_support_root):
            subdir = os.path.join(app_support_root, sub)
            if os.path.isdir(subdir):
                for candidate in ["Cache", "Local"]:
                    path = os.path.join(subdir, candidate)
                    if os.path.isdir(path):
                        dirs.append((get_size(path), path))

    # 按大小降序
    dirs.sort(reverse=True)
    return dirs

def clean_homebrew_cache():
    print("\n清理 Homebrew 缓存...")
    try:
        subprocess.run(["brew", "cleanup", "-s", "--quiet", "--prune=all"], check=False)
    except FileNotFoundError:
        print("⚠️ Homebrew 未安装或未加入 PATH")
    except subprocess.CalledProcessError:
        print("⚠️ Homebrew 清理失败")

def main():
    user_dirs = scan_user_caches()
    print("📊 用户缓存目录及大小（按大小排序）：")
    for size, path in user_dirs:
        print(f"{path}: {human_readable(size)}")

    confirm = input("\n⚠️ 是否清理以上缓存目录？(y/n): ")
    if confirm.lower() != 'y':
        print("已取消清理。")
        return

    total_before = sum(size for size, _ in user_dirs if size >= THRESHOLD)
    for size, path in user_dirs:
        if size >= THRESHOLD:
            print(f"清理: {path} ...")
            clean_cache(path)

    total_after = sum(get_size(p) for _, p in user_dirs if os.path.exists(p))
    released = total_before - total_after
    print(f"\n✅ 用户缓存清理完成，总共释放: {human_readable(released)}")

    # 清理 Homebrew 缓存
    clean_homebrew_cache()

if __name__ == "__main__":
    main()