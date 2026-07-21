#!/usr/bin/env bash
# ==========================================================
# fast_clean.sh - 开发者日常快速清理工具 (v2.0 优化版)
# ==========================================================
# 基于 diagnose_space.sh 诊断结果优化
# 新增: Xcode IB Support/Previews, npm cache, CoreSimulator
# 修复: 不再误删 Archives, Claude 只清缓存
# ==========================================================

set -uo pipefail

# -------------------- 辅助函数 --------------------
# 报告目录大小(MB)并返回，用于清理前后对比
get_size_mb() {
    local path="$1"
    if [ -e "$path" ]; then
        du -sm "$path" 2>/dev/null | awk '{print $1}'
    else
        echo 0
    fi
}

# 清理目录内容并报告释放空间
# 用法: clean_dir "项目名" "/path/to/dir"
clean_dir() {
    local name="$1"
    local path="$2"
    if [ ! -d "$path" ]; then
        echo "  ⊝  $name: 目录不存在，跳过"
        return
    fi
    local before
    before=$(get_size_mb "$path")
    if [ "$before" -eq 0 ]; then
        echo "  ⊝  $name: 已为空"
        return
    fi
    # 清理目录内容，保留目录本身
    rm -rf "${path:?}"/* 2>/dev/null
    rm -rf "${path:?}"/.* 2>/dev/null
    local after
    after=$(get_size_mb "$path")
    local freed=$((before - after))
    TOTAL_FREED=$((TOTAL_FREED + freed))
    printf "  ✅ %-28s 释放 %5d MB\n" "$name" "$freed"
}

# -------------------- 初始化 --------------------
TOTAL_FREED=0

echo "=========================================="
echo "🚀 快速清理模式启动 (v2.0)"
echo "=========================================="

# 统计开始空间
BEFORE=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')

# -------------------- 1. Xcode & 开发缓存 --------------------
echo ""
echo "📦 [1/6] Xcode 开发缓存"

clean_dir "DerivedData"          "$HOME/Library/Developer/Xcode/DerivedData"
clean_dir "iOS DeviceSupport"    "$HOME/Library/Developer/Xcode/iOS DeviceSupport"
clean_dir "IB Support"           "$HOME/Library/Developer/Xcode/UserData/IB Support"
clean_dir "Previews"             "$HOME/Library/Developer/Xcode/UserData/Previews"

# ⚠️ Archives 不再自动清理 - 包含发布签名归档，删除影响 App Store 上传
# 如需清理请手动执行: rm -rf ~/Library/Developer/Xcode/Archives/*

# 清理不可用的模拟器设备
echo "  🔄 删除不可用模拟器设备..."
xcrun simctl delete unavailable 2>/dev/null && echo "  ✅ simctl 清理完成" || echo "  ⊝  无可清理模拟器"

# -------------------- 2. Node.js 生态 --------------------
echo ""
echo "📦 [2/6] Node.js 缓存"

clean_dir "npm _cacache"         "$HOME/.npm/_cacache"
clean_dir "npm _npx"            "$HOME/.npm/_npx"

# npm cache clean 更彻底（清除全局缓存索引）
if command -v npm &>/dev/null; then
    echo "  🔄 执行 npm cache clean --force..."
    npm cache clean --force >/dev/null 2>&1 && echo "  ✅ npm cache 清理完成" || echo "  ⊝  npm cache 无需清理"
fi

# pnpm / yarn（如果存在）
clean_dir "pnpm store"          "$HOME/.pnpm-store"
clean_dir "yarn cache"          "$HOME/.yarn"

# -------------------- 3. 包管理器 --------------------
echo ""
echo "📦 [3/6] 包管理器缓存"

echo "  🔄 CocoaPods cache clean..."
pod cache clean --all >/dev/null 2>&1 && echo "  ✅ CocoaPods 清理完成" || echo "  ⊝  CocoaPods 无需清理"

echo "  🔄 Homebrew cleanup..."
brew cleanup -s >/dev/null 2>&1 && echo "  ✅ Homebrew 清理完成" || echo "  ⊝  Homebrew 无需清理"

clean_dir "Homebrew downloads"   "$HOME/Library/Caches/Homebrew/downloads"
clean_dir "pip cache"            "$HOME/Library/Caches/pip"

# -------------------- 4. Git 回收 --------------------
echo ""
echo "📦 [4/6] Git 仓库回收"

# 当前目录
if [ -d .git ]; then
    echo "  🔄 当前仓库 git gc..."
    git gc --prune=now >/dev/null 2>&1 && echo "  ✅ git gc 完成" || echo "  ⊝  git gc 无需操作"
else
    echo "  ⊝  当前目录不是 Git 仓库，跳过"
fi

# -------------------- 5. IDE & 浏览器缓存 --------------------
echo ""
echo "📦 [5/6] IDE & 浏览器缓存"

clean_dir "VSCode Cache"        "$HOME/Library/Application Support/Code/Cache"
clean_dir "VSCode CachedData"   "$HOME/Library/Application Support/Code/CachedData"
clean_dir "VSCode Code Cache"   "$HOME/Library/Application Support/Code/CachedExtensions"
clean_dir "Chrome cache"        "$HOME/Library/Caches/Google/Chrome"
clean_dir "Chrome Code Cache"   "$HOME/Library/Application Support/Google/Chrome/Default/Code Cache"

# Claude - 只清 Cache 子目录，不碰配置（修复安全隐患）
clean_dir "Claude Cache"        "$HOME/Library/Application Support/Claude/Cache"

# -------------------- 6. 微信 & 系统清理 --------------------
echo ""
echo "📦 [6/6] 微信 & 系统清理"

WECHAT_APP_DATA="$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents/app_data"
clean_dir "微信 log"             "$WECHAT_APP_DATA/log"
clean_dir "微信 radium"         "$WECHAT_APP_DATA/radium"

# 微信 Documents 大小报告（不自动删 - 避免误删聊天文件）
WECHAT_SIZE=$(du -sh "$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents" 2>/dev/null | awk '{print $1}')
echo "  ℹ️  微信 Documents 当前占用: ${WECHAT_SIZE}（建议在微信客户端内清理）"

# 用户日志
clean_dir "用户日志 Logs"       "$HOME/Library/Logs"

# 清空垃圾桶
echo "  🗑️  清空垃圾桶..."
TRASH_BEFORE=$(get_size_mb "$HOME/.Trash")
rm -rf ~/.Trash/* 2>/dev/null
rm -rf ~/.Trash/.* 2>/dev/null
TRASH_AFTER=$(get_size_mb "$HOME/.Trash")
TRASH_FREED=$((TRASH_BEFORE - TRASH_AFTER))
TOTAL_FREED=$((TOTAL_FREED + TRASH_FREED))
[ "$TRASH_FREED" -gt 0 ] && printf "  ✅ %-28s 释放 %5d MB\n" "垃圾桶" "$TRASH_FREED" || echo "  ⊝  垃圾桶已为空"

# -------------------- 汇总报告 --------------------
echo ""
echo "=========================================="
echo "✅ 清理完成！"
echo "------------------------------------------"
echo "📈 本次释放空间明细:"

AFTER=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')
DISK_DIFF=$((AFTER - BEFORE))

echo "  • 脚本统计清理总量: ${TOTAL_FREED} MB"
echo "  • 磁盘实际释放:     ${DISK_DIFF} MB"
echo "  • 当前可用空间:    $(df -h /System/Volumes/Data | awk 'NR==2 {print $4}')"

# 空间预警
FREE_GB=$(df -g /System/Volumes/Data | awk 'NR==2 {print $4}')
if [ "$FREE_GB" -lt 10 ]; then
    echo ""
    echo "  ⚠️  警告：剩余空间仅 ${FREE_GB}G，建议进一步清理:"
    echo "      • 微信客户端内清理聊天文件 (当前 ${WECHAT_SIZE})"
    echo "      • 检查 ~/Downloads 下载文件夹"
    echo "      • 运行 deep_clean.sh 进行深度清理"
fi
echo "=========================================="
