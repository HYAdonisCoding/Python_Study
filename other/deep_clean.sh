#!/usr/bin/env bash
# ==========================================================
# deep_clean.sh - macOS 全局深度清理器 (Version 2.3)
# ==========================================================

# -------------------- 颜色与工具 --------------------
info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }

get_size_mb() {
  local path="$1"
  if [ -d "$path" ]; then
    du -sm "$path" 2>/dev/null | awk '{print $1}'
  else
    echo 0
  fi
}

# -------------------- 自动扫描 JetBrains --------------------
# 动态识别所有版本的 IntelliJ/PyCharm/WebStorm 等
JETBRAINS_PATHS=$(ls -d $HOME/Library/Application\ Support/JetBrains/* 2>/dev/null || true)
JETBRAINS_CACHES=$(ls -d $HOME/Library/Caches/JetBrains/* 2>/dev/null || true)

# -------------------- 路径定义 --------------------
paths=(
  "System_Caches:$HOME/Library/Caches"
  "User_Logs:$HOME/Library/Logs"
  "Xcode_DerivedData:$HOME/Library/Developer/Xcode/DerivedData"
  "Xcode_Archives:$HOME/Library/Developer/Xcode/Archives"
  "Simulator_Devices:$HOME/Library/Developer/CoreSimulator/Devices"
  "Android_Caches:$HOME/Library/Caches/Google/AndroidStudio*"
  "VSCode_Cache:$HOME/Library/Application Support/Code/Cache"
  "Chrome_Cache:$HOME/Library/Caches/Google/Chrome"
  "Wallpaper_Cache:$HOME/Library/Application Support/com.apple.wallpaper"
  "Huawei_SDKs:$HOME/Library/Huawei"
)

# -------------------- 预扫描 --------------------
info "📊 深度清理预扫描："
total_before=0
for item in "${paths[@]}"; do
  path="${item#*:}"
  name="${item%%:*}"
  size=$(get_size_mb "$path")
  if [ "$size" -gt 1 ]; then
    printf "  %-25s %8s MB\n" "$name" "$size"
    total_before=$((total_before + size))
  fi
done

# 加入动态扫描的 JetBrains 大小
for jb in $JETBRAINS_PATHS $JETBRAINS_CACHES; do
  size=$(get_size_mb "$jb")
  total_before=$((total_before + size))
done

echo ""
read -p "⚠️  确认进行深度清理？此操作不可逆 (y/n): " confirm
[[ "$confirm" != "y" ]] && exit 0

# -------------------- 执行清理 --------------------
info "开始清理..."
for item in "${paths[@]}"; do
  path="${item#*:}"
  # 使用通配符安全清理内容，保留目录结构
  rm -rf ${path:?}/* 2>/dev/null && success "已清理: ${item%%:*}"
done

# 深度清理 JetBrains 旧版本
for jb in $JETBRAINS_PATHS $JETBRAINS_CACHES; do
  rm -rf "$jb" && success "已移除 JetBrains 目录: $(basename "$jb")"
done

# 重新初始化关键开发目录
mkdir -p ~/Library/Developer/Xcode/DerivedData
mkdir -p ~/Library/Developer/CoreSimulator/Devices

success "✅ 深度清理完成！"
info "累计释放空间约: ${total_before} MB"
info "当前磁盘状态："
df -h /System/Volumes/Data | grep /dev/disk