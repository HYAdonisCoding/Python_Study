#!/usr/bin/env bash
# ==========================================================
# deep_clean.sh - macOS 全局深度清理器 (v3.0)
# ==========================================================
# v3.0 变更（基于 2026-10-28 实战踩坑）:
#   1. 【致命修复】原 rm -rf ${path}/* 未加引号，含空格路径会被
#      shell 拆词（如 "Application Support"），等价于对
#      ~/Library/Application 单独执行 rm -rf，可能误删目录。
#      现统一改用 find "$path" -mindepth 1 ...，引号安全 + 覆盖隐藏文件
#   2. Xcode Archives 移出默认列表——存放 TestFlight 归档与 dSYM，
#      误删后旧崩溃日志无法符号化、旧包无法重传。
#      需要时显式加 --with-archives
#   3. 模拟器默认只删不可用设备（simctl delete unavailable），
#      整删全部设备数据需 --simulators-full
#   4. JetBrains 只删旧版本目录，保留最新版（避免当前 IDE 配置丢失）
#   5. 通配符路径（AndroidStudio*）改为循环处理，修复大小统计失效
#   6. 新增 --dry-run / --yes；两段式执行（先全量预览再动手）
#   7. wallpaper 与 Huawei SDK 改为显式开关，不再默认删除
# ==========================================================

set -uo pipefail

# -------------------- 参数解析 --------------------
DRY_RUN=0
ASSUME_YES=0
WITH_ARCHIVES=0
SIMULATORS_FULL=0
WITH_WALLPAPER=0
WITH_HUAWEI=0
for arg in "$@"; do
  case "$arg" in
    --dry-run)         DRY_RUN=1 ;;
    --yes|-y)          ASSUME_YES=1 ;;
    --with-archives)   WITH_ARCHIVES=1 ;;
    --simulators-full) SIMULATORS_FULL=1 ;;
    --wallpaper)       WITH_WALLPAPER=1 ;;
    --huawei)          WITH_HUAWEI=1 ;;
    *) echo "未知参数: $arg"; echo "支持: --dry-run --yes --with-archives --simulators-full --wallpaper --huawei"; exit 1 ;;
  esac
done

# -------------------- 日志 --------------------
LOG_DIR="$HOME/.clean_logs"
mkdir -p "$LOG_DIR" 2>/dev/null
LOG_FILE="$LOG_DIR/deep_clean_$(date +%Y%m%d_%H%M%S).log"
log_action() { echo "$(date '+%F %T') $1" >> "$LOG_FILE"; }

# -------------------- 辅助函数 --------------------
info()    { echo -e "\033[1;34m[INFO]\033[0m $1"; }
success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
warn()    { echo -e "\033[1;33m[WARN]\033[0m $1"; }

get_size_mb() {
  local path="$1" s
  if [ -e "$path" ]; then
    s=$(du -sm "$path" 2>/dev/null | awk '{print $1}')
    echo "${s:-0}"   # du 失败(如权限受限)时返回空，必须兜底为 0
  else
    echo 0
  fi
}

# 清空目录内容（保留目录本身）。引号安全，正确处理空格与隐藏文件。
wipe_path() {
  local name="$1" path="$2"
  if [ ! -d "$path" ]; then
    echo "  ⊝  $name: 目录不存在，跳过"
    return
  fi
  local before after freed
  before=$(get_size_mb "$path")
  if [ "$before" -eq 0 ]; then
    echo "  ⊝  $name: 已为空"
    return
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    printf "  [演练] %-28s 将清理 %6d MB\n" "$name" "$before"
    return
  fi
  find "$path" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null
  after=$(get_size_mb "$path")
  freed=$((before - after))
  TOTAL_FREED=$((TOTAL_FREED + freed))
  log_action "CLEAN $name freed=${freed}MB path=$path"
  printf "  ✅ %-30s 释放 %6d MB\n" "$name" "$freed"
}

# 整目录删除（用于旧版本残留等）
remove_dir() {
  local name="$1" path="$2"
  if [ ! -d "$path" ]; then
    echo "  ⊝  $name: 目录不存在，跳过"
    return
  fi
  local sz
  sz=$(get_size_mb "$path")
  if [ "$DRY_RUN" -eq 1 ]; then
    printf "  [演练] %-28s 将删除 %6d MB\n" "$name" "$sz"
    return
  fi
  rm -rf "$path"
  TOTAL_FREED=$((TOTAL_FREED + sz))
  log_action "REMOVE $name freed=${sz}MB path=$path"
  printf "  ✅ %-30s 释放 %6d MB\n" "$name" "$sz"
}

# JetBrains: 保留最新版本目录，删除旧版本（配置与索引随版本走）
clean_jetbrains_old() {
  local base="$1" label="$2"
  [ -d "$base" ] || return 0
  local latest
  latest=$(ls "$base" 2>/dev/null | sort -r | head -n 1)
  [ -n "$latest" ] || return 0
  local d sz
  for d in "$base"/*; do
    [ -d "$d" ] || continue
    if [ "$(basename "$d")" = "$latest" ]; then
      echo "  ⊝  保留最新 $label: $latest"
      continue
    fi
    remove_dir "$label 旧版 $(basename "$d")" "$d"
  done
}

# -------------------- 执行清单 --------------------
run_all() {
  # ===== 默认清理（纯缓存/可再生）=====
  echo ""
  info "【默认清理】纯缓存与可再生数据："
  wipe_path "System_Caches"   "$HOME/Library/Caches"
  wipe_path "User_Logs"       "$HOME/Library/Logs"
  wipe_path "Xcode_DerivedData" "$HOME/Library/Developer/Xcode/DerivedData"
  wipe_path "VSCode_Cache"    "$HOME/Library/Application Support/Code/Cache"
  wipe_path "Chrome_Cache"    "$HOME/Library/Caches/Google/Chrome"

  # Android Studio 缓存（通配符逐个处理，避免统计失效）
  local d
  for d in "$HOME/Library/Caches/Google/"AndroidStudio*; do
    [ -d "$d" ] || continue
    wipe_path "Android_Cache $(basename "$d")" "$d"
  done

  # ===== 可选清理（显式开关）=====
  echo ""
  info "【可选清理】按开关执行："

  if [ "$WITH_ARCHIVES" -eq 1 ]; then
    warn "Xcode_Archives 将被清空——TestFlight 归档与 dSYM 不可恢复！"
    wipe_path "Xcode_Archives" "$HOME/Library/Developer/Xcode/Archives"
  else
    local arc_sz
    arc_sz=$(get_size_mb "$HOME/Library/Developer/Xcode/Archives")
    echo "  ⊝  Xcode_Archives: ${arc_sz} MB（保留，加 --with-archives 清理）"
  fi

  if [ "$SIMULATORS_FULL" -eq 1 ]; then
    warn "将删除全部模拟器设备数据！"
    wipe_path "Simulator_Devices" "$HOME/Library/Developer/CoreSimulator/Devices"
  else
    echo "  🔄 simctl 删除不可用模拟器设备（保留可用设备）..."
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "  [演练] xcrun simctl delete unavailable"
    else
      xcrun simctl delete unavailable 2>/dev/null \
        && success "simctl 清理完成" \
        || echo "  ⊝  无可清理模拟器"
    fi
  fi

  if [ "$WITH_WALLPAPER" -eq 1 ]; then
    wipe_path "Wallpaper_Cache" "$HOME/Library/Application Support/com.apple.wallpaper"
  else
    local wp_sz
    wp_sz=$(get_size_mb "$HOME/Library/Application Support/com.apple.wallpaper")
    echo "  ⊝  Wallpaper_Cache: ${wp_sz} MB（保留，加 --wallpaper 清理，删后壁纸可能重置）"
  fi

  if [ "$WITH_HUAWEI" -eq 1 ]; then
    wipe_path "Huawei_SDKs" "$HOME/Library/Huawei"
  else
    local hw_sz
    hw_sz=$(get_size_mb "$HOME/Library/Huawei")
    echo "  ⊝  Huawei_SDKs: ${hw_sz} MB（保留，加 --huawei 清理）"
  fi

  # ===== JetBrains 旧版本 =====
  echo ""
  info "【JetBrains】只删旧版本，保留当前在用版本："
  clean_jetbrains_old "$HOME/Library/Application Support/JetBrains" "配置"
  clean_jetbrains_old "$HOME/Library/Caches/JetBrains" "缓存"

  # ===== 收尾：重建关键开发目录 =====
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$HOME/Library/Developer/Xcode/DerivedData"
    mkdir -p "$HOME/Library/Developer/CoreSimulator/Devices"
  fi
}

# -------------------- 主流程：先演练，再执行 --------------------
TOTAL_FREED=0
REQUEST_DRY_RUN=$DRY_RUN
BEFORE_MB=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')

echo "=========================================="
echo "🧹 深度清理器 v3.0（两段式：先预览后执行）"
echo "=========================================="

# 第一遍：演练，展示将清理的内容
DRY_RUN=1
run_all

echo ""
if [ "$REQUEST_DRY_RUN" -eq 1 ]; then
  info "演练结束（--dry-run），未删除任何文件。"
  exit 0
fi

# 确认
if [ "$ASSUME_YES" -eq 1 ]; then
  warn "已指定 --yes，跳过确认直接执行。"
else
  echo ""
  read -rp "⚠️  确认执行以上深度清理？此操作不可逆 (y/n): " confirm
  if [[ "$confirm" != "y" ]]; then
    info "已取消，未删除任何文件。"
    exit 0
  fi
fi

# 第二遍：真删
TOTAL_FREED=0
DRY_RUN=0
run_all

# -------------------- 汇总 --------------------
AFTER_MB=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')
DISK_DIFF=$((AFTER_MB - BEFORE_MB))

echo ""
success "✅ 深度清理完成！"
info "本次统计清理总量: ${TOTAL_FREED} MB"
info "磁盘实际释放(参考): ${DISK_DIFF} MB"
info "当前磁盘可用: $(df -h /System/Volumes/Data | awk 'NR==2 {print $4}')"
info "操作日志: $LOG_FILE"
