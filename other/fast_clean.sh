#!/usr/bin/env bash
# ==========================================================
# fast_clean.sh - 开发者日常快速清理工具
# ==========================================================

echo "------------------------------------------"
echo "🚀 快速清理模式启动..."

# 统计开始空间
BEFORE=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')

# 1. Xcode & 模拟器 (核心回血区)
echo "🧹 清理 Xcode 派生数据与缓存..."
rm -rf ~/Library/Developer/Xcode/DerivedData/*
rm -rf ~/Library/Developer/Xcode/Archives/*
rm -rf ~/Library/Developer/Xcode/iOS\ DeviceSupport/*
xcrun simctl delete unavailable 2>/dev/null

# 2. 开发者工具缓存
echo "🧹 清理 CocoaPods & Homebrew 缓存..."
pod cache clean --all >/dev/null 2>&1 || true
brew cleanup -s >/dev/null 2>&1 || true

# 3. 异常占用应用 (根据你的扫描结果定制)
echo "🧹 清理应用缓存 (Claude/微信资源)..."
# Claude 缓存
rm -rf ~/Library/Application\ Support/Claude/* 2>/dev/null
# 微信资源文件 (安全清理，不删数据库)
find ~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application\ Support/com.tencent.xinWeChat -name "MessageTemp" -type d -exec rm -rf {} + 2>/dev/null

# 4. 强制清空垃圾桶 (释放占位)
echo "🗑️  清空垃圾桶..."
rm -rf ~/.Trash/* 2>/dev/null

# 统计结束空间
AFTER=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')
DIFF=$((AFTER - BEFORE))

echo "------------------------------------------"
echo "✅ 清理完成！"
echo "📈 本次为您释放空间: ${DIFF} MB"
echo "📊 当前可用空间: $(df -h /System/Volumes/Data | awk 'NR==2 {print $4}')"
echo "------------------------------------------"