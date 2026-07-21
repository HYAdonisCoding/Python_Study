#!/usr/bin/env bash
# ==========================================================
# diagnose_space.sh - 只读诊断：列出各清理项占用空间
# ==========================================================
# 不会删除任何文件，仅扫描大小

set -uo pipefail

# 存储结果：大小MB 路径
declare -a RESULTS

scan() {
    local name="$1"
    local path="$2"
    if [ -e "$path" ]; then
        local size_mb
        size_mb=$(du -sm "$path" 2>/dev/null | awk '{print $1}')
        if [ -n "$size_mb" ] && [ "$size_mb" -gt 0 ]; then
            RESULTS+=("$size_mb|$name|$path")
        fi
    fi
}

echo "=========================================="
echo "📊 磁盘占用诊断扫描（只读，不删除任何文件）"
echo "=========================================="
echo ""

# --- Xcode 相关 ---
scan "Xcode DerivedData"          "$HOME/Library/Developer/Xcode/DerivedData"
scan "Xcode Archives"             "$HOME/Library/Developer/Xcode/Archives"
scan "Xcode iOS DeviceSupport"    "$HOME/Library/Developer/Xcode/iOS DeviceSupport"
scan "CoreSimulator Devices"      "$HOME/Library/Developer/CoreSimulator/Devices"
scan "Xcode Playgrounds"          "$HOME/Library/Developer/Xcode/UserData"

# --- iOS Simulator Runtime 镜像 ---
echo "🔍 扫描 iOS Simulator Runtime..."
RUNTIME_SIZE=$(du -sm "$HOME/Library/Developer/CoreSimulator/Images" 2>/dev/null | awk '{print $1}')
[ -n "$RUNTIME_SIZE" ] && [ "$RUNTIME_SIZE" -gt 0 ] && RESULTS+=("$RUNTIME_SIZE|Simulator Runtime Images|$HOME/Library/Developer/CoreSimulator/Images")

# --- Node.js 生态 ---
scan "npm cache"                  "$HOME/.npm"
scan "npm cache (_cacache)"       "$HOME/.npm/_cacache"
scan "pnpm store"                 "$HOME/.pnpm-store"
scan "pnpm store (v3)"            "$HOME/Library/pnpm/store"
scan "yarn cache"                 "$HOME/.yarn"
scan "node_modules (Home)"        "$HOME/.node-gyp"

# --- Python ---
scan "pip cache"                  "$HOME/Library/Caches/pip"
scan "pip cache (.cache)"         "$HOME/.cache/pip"
scan "uv cache"                  "$HOME/.cache/uv"

# --- Android / Java ---
scan "Gradle caches"              "$HOME/.gradle/caches"
scan "Maven repository"           "$HOME/.m2/repository"
scan "Android SDK"                "$HOME/Library/Android/sdk"

# --- Go / Rust ---
scan "Go module cache"            "$HOME/go/pkg/mod"
scan "Cargo cache"                "$HOME/.cargo/registry"

# --- 包管理器 ---
scan "Homebrew cache"             "$HOME/Library/Caches/Homebrew"
scan "CocoaPods cache"            "$HOME/Library/Caches/CocoaPods"

# --- 浏览器 & IDE ---
scan "Chrome cache"               "$HOME/Library/Caches/Google/Chrome"
scan "VSCode Cache"               "$HOME/Library/Application Support/Code/Cache"
scan "VSCode CachedData"          "$HOME/Library/Application Support/Code/CachedData"
scan "VSCode Code Cache"          "$HOME/Library/Application Support/Code/CachedExtensions"
scan "JetBrains Caches"           "$HOME/Library/Caches/JetBrains"

# --- 日志 & 崩溃报告 ---
scan "用户日志 Library/Logs"       "$HOME/Library/Logs"
scan "DiagnosticReports"          "$HOME/Library/Logs/DiagnosticReports"

# --- 系统缓存 ---
scan "用户级 Caches"               "$HOME/Library/Caches"
scan "系统临时文件 /tmp"           "/tmp"

# --- 微信 ---
scan "微信 Documents"             "$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents"
scan "微信 app_data"               "$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents/app_data"

# --- 其他 ---
scan "垃圾桶 Trash"               "$HOME/.Trash"
scan "Claude App Support"         "$HOME/Library/Application Support/Claude"
scan "Downloads"                  "$HOME/Downloads"

# --- Docker (如果装了) ---
if command -v docker &>/dev/null; then
    echo "🐳 检测到 Docker，扫描占用..."
    DOCKER_SIZE=$(docker system df --format '{{.Size}}' 2>/dev/null | head -1)
    [ -n "$DOCKER_SIZE" ] && echo "   Docker: $DOCKER_SIZE"
fi

# --- 排序输出 ---
echo ""
echo "=========================================="
echo "📈 各项目占用空间（从大到小排序）"
echo "=========================================="
printf "%-10s %-35s %s\n" "大小(MB)" "项目" "路径"
echo "------------------------------------------------------------"

# 按大小排序
printf '%s\n' "${RESULTS[@]}" | sort -t'|' -k1 -rn | while IFS='|' read -r size name path; do
    printf "%-10s %-35s %s\n" "$size" "$name" "$path"
done

# --- 汇总 ---
TOTAL=0
for item in "${RESULTS[@]}"; do
    size=$(echo "$item" | cut -d'|' -f1)
    TOTAL=$((TOTAL + size))
done

echo "------------------------------------------------------------"
echo "📊 扫描到的可清理总量约: ${TOTAL} MB ($(( TOTAL / 1024 )) GB)"
echo ""
echo "ℹ️ 注意: 部分项目有重叠（如 Caches 包含子项），总量可能偏高"
echo "ℹ️ 磁盘真实可用空间:"
df -h /System/Volumes/Data | awk 'NR==1 {print "   "$0} NR==2 {print "   "$0}'
