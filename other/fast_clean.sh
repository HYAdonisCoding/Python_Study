#!/bin/bash

# 移除 set -e，改用更灵活的执行方式
echo "------------------------------------------"
echo "🚀 开始深度清理 Mac 开发环境..."
date
echo "------------------------------------------"

# 获取清理前的空间
BEFORE=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')

# 定义清理函数
clean_dir() {
    if [ -d "$1" ]; then
        # 统计文件夹大小
        SIZE=$(du -sh "$1" 2>/dev/null | awk '{print $1}')
        echo "🧹 正在清理 ($SIZE): $1"
        # 使用 -f 强制删除，避免因找不到文件而报错
        rm -rf "$1"/* 2>/dev/null
    else
        echo "[跳过] 目录不存在: $1"
    fi
}

# 1. Xcode 相关
clean_dir "$HOME/Library/Developer/Xcode/DerivedData"
clean_dir "$HOME/Library/Developer/Xcode/Archives"
clean_dir "$HOME/Library/Developer/Xcode/iOS DeviceSupport"
echo "🔧 正在移除不可用的模拟器数据..."
xcrun simctl delete unavailable 2>/dev/null

# 2. 软件残余
clean_dir "$HOME/Library/Application Support/Claude"
clean_dir "$HOME/Library/Application Support/yuque-desktop"
if [ -d "$HOME/Library/Application Support/JetBrains" ]; then
    echo "🧹 正在彻底移除 JetBrains 残余..."
    rm -rf "$HOME/Library/Application Support/JetBrains" 2>/dev/null
    rm -rf "$HOME/Library/Caches/JetBrains" 2>/dev/null
fi

# 3. 包管理器 (静默执行)
echo "📦 正在清理 CocoaPods 与 Homebrew 缓存..."
pod cache clean --all >/dev/null 2>&1 || echo "⚠️ Pods 清理跳过"
brew cleanup -s >/dev/null 2>&1 || echo "⚠️ Brew 清理跳过"

# 4. 终极一击：清空垃圾桶
echo "🗑️ 正在清空系统垃圾桶..."
rm -rf ~/.Trash/* 2>/dev/null

# 统计战果
AFTER=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')
DIFF=$((AFTER - BEFORE))

echo "------------------------------------------"
echo "✅ 清理完成！"
echo "📈 本次为您腾出空间: ${DIFF} MB"
echo "📊 当前可用空间："
df -h /System/Volumes/Data | grep /dev/disk
echo "------------------------------------------"