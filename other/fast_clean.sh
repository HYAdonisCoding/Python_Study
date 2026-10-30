#!/usr/bin/env bash
# ==========================================================
# fast_clean.sh - 开发者日常快速清理工具 (v3.0)
# ==========================================================
# v3.0 变更（基于 2026-10-28 实战踩坑）:
#   1. 修复: rm -rf dir/.* 会匹配 . 与 .. 的隐患，
#      统一改用 find -mindepth 1 精确删除（含隐藏文件）
#   2. iOS DeviceSupport 默认跳过——删一次重下 4.6GB，
#      需要时显式加 --device-support
#   3. yarn 只清 ~/.yarn/cache，不再整删 ~/.yarn（含全局配置）
#   4. 清空废纸篓前单独二次确认（不可逆操作）
#   5. 微信 radium 拆分：web 子目录(浏览器缓存)默认清，
#      users 子目录(头像/已下载聊天文件)改为 --wechat-users 显式清理
#   6. 新增 --dry-run（演练）/ --yes（跳过确认）/ --device-support
#   7. get_size_mb 空值兜底，修复 du 失败时 "integer expected" 报错
#   8. 所有实际删除动作写入日志 ~/.clean_logs/
# ==========================================================

set -uo pipefail

# -------------------- 参数解析 --------------------
DRY_RUN=0
ASSUME_YES=0
CLEAN_DEVICE_SUPPORT=0
CLEAN_WECHAT_USERS=0
for arg in "$@"; do
  case "$arg" in
    --dry-run)        DRY_RUN=1 ;;
    --yes|-y)         ASSUME_YES=1 ;;
    --device-support) CLEAN_DEVICE_SUPPORT=1 ;;
    --wechat-users)   CLEAN_WECHAT_USERS=1 ;;
    *) echo "未知参数: $arg（支持 --dry-run / --yes / --device-support / --wechat-users）"; exit 1 ;;
  esac
done

warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }

# -------------------- 日志 --------------------
LOG_DIR="$HOME/.clean_logs"
mkdir -p "$LOG_DIR" 2>/dev/null
LOG_FILE="$LOG_DIR/fast_clean_$(date +%Y%m%d_%H%M%S).log"
log_action() { echo "$(date '+%F %T') $1" >> "$LOG_FILE"; }

# -------------------- 辅助函数 --------------------
get_size_mb() {
    local path="$1" s
    if [ -e "$path" ]; then
        s=$(du -sm "$path" 2>/dev/null | awk '{print $1}')
        echo "${s:-0}"   # du 失败(如权限受限)时返回空，必须兜底为 0
    else
        echo 0
    fi
}

# 清理目录内容并报告释放空间（保留目录本身）
# 用法: clean_dir "项目名" "/path/to/dir"
clean_dir() {
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
        printf "  [演练] %-26s 将清理 %6d MB\n" "$name" "$before"
        return
    fi
    # find 方式：正确处理空格路径与隐藏文件，且不会碰 . 和 ..
    find "$path" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null
    after=$(get_size_mb "$path")
    freed=$((before - after))
    TOTAL_FREED=$((TOTAL_FREED + freed))
    log_action "CLEAN $name freed=${freed}MB path=$path"
    printf "  ✅ %-28s 释放 %5d MB\n" "$name" "$freed"
}

# 执行外部命令并统一回报（npm/brew/pod/git/simctl 等）
# 用法: run_cmd "描述" 命令 参数...
run_cmd() {
    local desc="$1"; shift
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "  [演练] $desc: $*"
        return
    fi
    if "$@" >/dev/null 2>&1; then
        log_action "RUN $desc ok: $*"
        echo "  ✅ $desc 完成"
    else
        echo "  ⊝  $desc 无需清理/跳过"
    fi
}

# -------------------- 初始化 --------------------
TOTAL_FREED=0

echo "=========================================="
echo "🚀 快速清理模式启动 (v3.0)  $([ $DRY_RUN -eq 1 ] && echo '【演练模式，不实际删除】')"
echo "=========================================="

# 统计开始空间
BEFORE=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')

# -------------------- 1. Xcode & 开发缓存 --------------------
echo ""
echo "📦 [1/6] Xcode 开发缓存"

clean_dir "DerivedData"          "$HOME/Library/Developer/Xcode/DerivedData"
clean_dir "IB Support"           "$HOME/Library/Developer/Xcode/UserData/IB Support"
clean_dir "Previews"             "$HOME/Library/Developer/Xcode/UserData/Previews"

# ⚠️ Archives 永不自动清理 - 包含发布签名归档与 dSYM
# 误删后：TestFlight 归档丢失、旧崩溃日志无法符号化。请手动确认后再删。

# iOS DeviceSupport：默认保留（重删一次要重下 ~4.6GB）
if [ "$CLEAN_DEVICE_SUPPORT" -eq 1 ]; then
    clean_dir "iOS DeviceSupport"    "$HOME/Library/Developer/Xcode/iOS DeviceSupport"
else
    DS_SIZE=$(get_size_mb "$HOME/Library/Developer/Xcode/iOS DeviceSupport")
    [ "$DS_SIZE" -gt 0 ] && echo "  ⊝  iOS DeviceSupport: ${DS_SIZE} MB（默认保留，加 --device-support 清理）"
fi

# 清理不可用的模拟器设备（保留可用设备数据，安全）
run_cmd "simctl 删除不可用模拟器" xcrun simctl delete unavailable

# -------------------- 2. Node.js 生态 --------------------
echo ""
echo "📦 [2/6] Node.js 缓存"

clean_dir "npm _cacache"         "$HOME/.npm/_cacache"
clean_dir "npm _npx"            "$HOME/.npm/_npx"

if command -v npm &>/dev/null; then
    run_cmd "npm cache clean" npm cache clean --force
fi

# pnpm（如果存在）
clean_dir "pnpm store"          "$HOME/.pnpm-store"
# ⚠️ v3.0 修复：只清缓存子目录，~/.yarn 含 yarnrc 与全局安装
clean_dir "yarn cache"          "$HOME/.yarn/cache"
if command -v yarn &>/dev/null; then
    run_cmd "yarn cache clean" yarn cache clean
fi

# -------------------- 3. 包管理器 --------------------
echo ""
echo "📦 [3/6] 包管理器缓存"

if command -v pod &>/dev/null; then
    run_cmd "CocoaPods cache clean" pod cache clean --all
fi
if command -v brew &>/dev/null; then
    run_cmd "Homebrew cleanup" brew cleanup -s
fi

clean_dir "Homebrew downloads"   "$HOME/Library/Caches/Homebrew/downloads"
clean_dir "pip cache"            "$HOME/Library/Caches/pip"

# -------------------- 4. Git 回收 --------------------
echo ""
echo "📦 [4/6] Git 仓库回收"

if [ -d .git ]; then
    run_cmd "当前仓库 git gc" git gc --prune=now
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

# Claude - 只清 Cache 子目录，不碰配置
clean_dir "Claude Cache"        "$HOME/Library/Application Support/Claude/Cache"

# -------------------- 6. 微信 & 系统清理 --------------------
echo ""
echo "📦 [6/6] 微信 & 系统清理"

WECHAT_APP_DATA="$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents/app_data"
# ⚠️ v3.0 修复：radium 不再整删。拆分为：
#   radium/web   = 微信内置浏览器缓存，安全，默认清
#   radium/users = 账号数据（头像、已下载的聊天文件），默认保留，--wechat-users 才清
clean_dir "微信 log"             "$WECHAT_APP_DATA/log"
clean_dir "微信 radium/web"      "$WECHAT_APP_DATA/radium/web"

if [ "$CLEAN_WECHAT_USERS" -eq 1 ]; then
    warn "  ⚠️  将清理 radium/users：账号头像与已下载聊天文件缓存"
    clean_dir "微信 radium/users"    "$WECHAT_APP_DATA/radium/users"
else
    WU_SIZE=$(get_size_mb "$WECHAT_APP_DATA/radium/users")
    echo "  ⊝  微信 radium/users: ${WU_SIZE} MB（保留账号资产，加 --wechat-users 清理）"
fi

# 微信 Documents 大小报告（不自动删 - 避免误删聊天文件）
WECHAT_SIZE=$(du -sh "$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents" 2>/dev/null | awk '{print $1}')
echo "  ℹ️  微信 Documents 当前占用: ${WECHAT_SIZE}（建议在微信客户端内清理）"

# 用户日志
clean_dir "用户日志 Logs"       "$HOME/Library/Logs"

# 清空垃圾桶（不可逆，单独二次确认）
TRASH_BEFORE=$(get_size_mb "$HOME/.Trash")
if [ "$TRASH_BEFORE" -gt 0 ]; then
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "  [演练] 垃圾桶: 将清空 ${TRASH_BEFORE} MB（不可逆）"
    else
        DO_TRASH=0
        if [ "$ASSUME_YES" -eq 1 ]; then
            DO_TRASH=1
        else
            read -rp "  ⚠️  清空废纸篓 ${TRASH_BEFORE} MB？不可恢复 (y/n): " ans
            [[ "$ans" == "y" ]] && DO_TRASH=1
        fi
        if [ "$DO_TRASH" -eq 1 ]; then
            find "$HOME/.Trash" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null
            TRASH_AFTER=$(get_size_mb "$HOME/.Trash")
            TRASH_FREED=$((TRASH_BEFORE - TRASH_AFTER))
            TOTAL_FREED=$((TOTAL_FREED + TRASH_FREED))
            log_action "EMPTY_TRASH freed=${TRASH_FREED}MB"
            printf "  ✅ %-28s 释放 %5d MB\n" "垃圾桶" "$TRASH_FREED"
        else
            echo "  ⊝  垃圾桶：跳过（${TRASH_BEFORE} MB 仍占用）"
        fi
    fi
else
    echo "  ⊝  垃圾桶已为空"
fi

# -------------------- 汇总报告 --------------------
echo ""
echo "=========================================="
echo "✅ 清理完成！"
echo "------------------------------------------"
echo "📈 本次释放空间明细:"

AFTER=$(df -m /System/Volumes/Data | awk 'NR==2 {print $4}')
DISK_DIFF=$((AFTER - BEFORE))

echo "  • 脚本统计清理总量: ${TOTAL_FREED} MB"
echo "  • 磁盘实际释放(参考): ${DISK_DIFF} MB"
echo "  • 当前可用空间:      $(df -h /System/Volumes/Data | awk 'NR==2 {print $4}')"
echo "  • 操作日志:          $LOG_FILE"

# 空间预警
FREE_GB=$(df -g /System/Volumes/Data | awk 'NR==2 {print $4}')
if [ "$FREE_GB" -lt 10 ]; then
    echo ""
    echo "  ⚠️  警告：剩余空间仅 ${FREE_GB}G，建议进一步清理:"
    echo "      • 微信客户端内清理聊天文件 (当前 ${WECHAT_SIZE})"
    echo "      • 检查 ~/Downloads 下载文件夹"
    echo "      • 运行 deep_clean.sh --dry-run 查看深度清理预览"
fi
echo "=========================================="
