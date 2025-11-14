#!/usr/bin/env bash
# ==========================================================
# macOS 全局缓存清理器 (系统 + 开发工具 + 办公软件)
# Author: Eason
# Version: 2.1
# ==========================================================

set -e

# -------------------- 颜色输出 --------------------
function info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
function warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }
function success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
function error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# -------------------- 工具函数 --------------------
function get_dir_size_bytes() {
  local dir="$1"
  if [ -d "$dir" ]; then
    du -sk "$dir" 2>/dev/null | awk '{print $1 * 1024}'
  else
    echo 0
  fi
}

function human_readable() {
  local bytes=$1
  if (( bytes < 1024 )); then
    echo "${bytes} B"
  elif (( bytes < 1048576 )); then
    echo "$((bytes / 1024)) KB"
  elif (( bytes < 1073741824 )); then
    echo "$((bytes / 1048576)) MB"
  else
    printf "%.2f GB" "$(echo "$bytes / 1073741824" | bc -l)"
  fi
}

# -------------------- 缓存路径 --------------------
declare -A all_paths=(
  # 系统缓存
  [System_Cache]="$HOME/Library/Caches"
  [Library_Caches]="/Library/Caches"
  [Private_Folders]="/private/var/folders"
  [User_Logs]="$HOME/Library/Logs"
  [Trash]="$HOME/.Trash"
  [Temp_Files]="/tmp"
  [Safari_Cache]="$HOME/Library/Caches/com.apple.Safari"
  [Chrome_Cache]="$HOME/Library/Caches/Google/Chrome"
  [Firefox_Cache]="$HOME/Library/Caches/Firefox"
  [Homebrew_Cache]="$HOME/Library/Caches/Homebrew"

  # 开发工具
  [Xcode_DerivedData]="$HOME/Library/Developer/Xcode/DerivedData"
  [Xcode_Archives]="$HOME/Library/Developer/Xcode/Archives"
  [Xcode_DeviceSupport]="$HOME/Library/Developer/Xcode/iOS DeviceSupport"
  [Xcode_DocumentationCache]="$HOME/Library/Developer/Xcode/DocumentationCache"
  [CoreSimulator_Devices]="$HOME/Library/Developer/CoreSimulator/Devices"
  [CoreSimulator_Caches]="$HOME/Library/Developer/CoreSimulator/Caches"
  [AndroidStudio_Caches]="$HOME/Library/Caches/AndroidStudio"
  [AndroidStudio_Config]="$HOME/Library/Application Support/Google/AndroidStudio"
  [IntelliJ_Caches]="$HOME/Library/Caches/IntelliJIdea"
  [IntelliJ_Config]="$HOME/Library/Application Support/JetBrains/IntelliJIdea2023.1"
  [VSCode_Caches]="$HOME/Library/Application Support/Code/Cache"
  [VSCode_UserData]="$HOME/Library/Application Support/Code/User"

  # 办公软件
  [Sublime_Text_Caches]="$HOME/Library/Application Support/Sublime Text 3/Cache"
  [Typora_Caches]="$HOME/Library/Application Support/abnerworks.Typora"
  [MWeb_Caches]="$HOME/Library/Containers/com.coderforart.MWeb/Data/Library/Caches"
  [MWeb_Config]="$HOME/Library/Containers/com.coderforart.MWeb/Data/Library/Application Support"
  [Microsoft_Office_Caches]="$HOME/Library/Containers/com.microsoft.Office/Data/Library/Caches"
  [Microsoft_Office_AppSupport]="$HOME/Library/Containers/com.microsoft.Office/Data/Library/Application Support"
  [WPS_Caches]="$HOME/Library/Containers/com.kingsoft.wpsoffice.mac/Data/Library/Caches"
  [WPS_Config]="$HOME/Library/Containers/com.kingsoft.wpsoffice.mac/Data/Library/Application Support"
)

# -------------------- 打印清理前占用 --------------------
info "📊 当前主要缓存目录占用空间："
total_before=0
for key in "${!all_paths[@]}"; do
  path="${all_paths[$key]}"
  display_name="${key//_/ }"
  if [ -d "$path" ]; then
    size_bytes=$(get_dir_size_bytes "$path")
    if [ "$size_bytes" -gt 0 ]; then
      size=$(du -sh "$path" 2>/dev/null | awk '{print $1}')
      total_before=$((total_before + size_bytes))
      printf "  %-30s %10s\n" "$display_name" "$size"
    fi
  fi
done

echo ""
read -rp "⚠️  是否继续清理以上缓存？(y/n): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  warn "已取消清理。"
  exit 0
fi

# -------------------- 清理函数 --------------------
function clean_path() {
  local key="$1"
  local path="$2"
  local display_name="${key//_/ }"

  if [ ! -e "$path" ]; then return; fi
  if [ ! -w "$path" ]; then
    warn "跳过无权限删除: $display_name"
    return
  fi

  # 容器应用安全清理
  if [[ "$key" =~ Safari|Office|MWeb|WPS ]]; then
    backup="$path.bak.$(date +%s)"
    mv "$path" "$backup" 2>/dev/null && mkdir -p "$path"
    (sleep 2; rm -rf "$backup") &
    success "已清理：$display_name"
    return
  fi

  # 普通目录直接删除内容
  if [ -d "$path" ]; then
    if [ "$(ls -A "$path" 2>/dev/null)" ]; then
      rm -rf "$path"/.[!.]* "$path"/* 2>/dev/null || true
      success "已清理：$display_name"
    fi
  elif [ -f "$path" ]; then
    rm -f "$path" 2>/dev/null && success "已清理：$display_name"
  fi
}

# -------------------- 执行清理 --------------------
info "开始清理缓存..."
for key in "${!all_paths[@]}"; do
  clean_path "$key" "${all_paths[$key]}"
done

# 重新创建关键目录（防止 Xcode/CoreSimulator 崩溃）
mkdir -p "$HOME/Library/Developer/Xcode/DerivedData"
mkdir -p "$HOME/Library/Developer/CoreSimulator/Devices"
mkdir -p "$HOME/Library/Developer/CoreSimulator/Caches"

# -------------------- 计算释放空间 --------------------
total_after=0
for path in "${all_paths[@]}"; do
  size=$(get_dir_size_bytes "$path" 2>/dev/null || echo 0)
  total_after=$((total_after + size))
done

released=$((total_before - total_after))
echo ""
success "✅ 全局清理完成！"
info "共释放磁盘空间：$(human_readable $released)"
info "建议重新启动 Xcode 或计算机以使缓存彻底刷新。"