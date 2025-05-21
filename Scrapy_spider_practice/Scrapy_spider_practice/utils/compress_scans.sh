#!/bin/bash

# ========= 参数 =========
TARGET_DIR="$1"
SCAN_QUALITY=70
NORMAL_QUALITY=85
MAX_DIM_SCAN=2000
MAX_DIM_NORMAL=3000

# ========= 校验 =========
if [ -z "$TARGET_DIR" ]; then
  echo "❌ 请提供图片目录路径"
  echo "✅ 示例：./smart_compress_with_stats.sh /Users/eason/Pictures"
  exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
  echo "❌ 无效目录：$TARGET_DIR"
  exit 1
fi

echo "📁 开始压缩目录：$TARGET_DIR"
echo "------------------------------"

# ========= 压缩函数 =========
compress_image() {
  local file="$1"
  local strategy="$2"
  local quality="$3"
  local max_dim="$4"

  local orig_size_kb=$(du -k "$file" | cut -f1)

  # 使用临时文件中转以便计算压缩前后体积
  local tmp_file="${file}.tmp"
  convert "$file" -resize ${max_dim}x${max_dim}\> -quality $quality -strip "$tmp_file"

  local new_size_kb=$(du -k "$tmp_file" | cut -f1)
  local saved_kb=$((orig_size_kb - new_size_kb))
  local percent=$((100 * saved_kb / orig_size_kb))

  # 覆盖原图
  mv "$tmp_file" "$file"

  # 打印结果
  printf "%-30s | %-6s → %-6s KB | saved: %-6s KB (%2d%%)\n" "$(basename "$file")" "$orig_size_kb" "$new_size_kb" "$saved_kb" "$percent"
}

# ========= 主体 =========
find "$TARGET_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r file; do
  filename=$(basename "$file")

  if [[ "$filename" == *扫描* ]]; then
    compress_image "$file" "扫描" "$SCAN_QUALITY" "$MAX_DIM_SCAN"
  else
    compress_image "$file" "普通" "$NORMAL_QUALITY" "$MAX_DIM_NORMAL"
  fi
done

echo "------------------------------"
echo "✅ 所有图片压缩完成并显示节省空间情况"