#!/bin/bash

# 检查是否安装了 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ 错误: 未检测到 ffmpeg，请先执行 'brew install ffmpeg' 安装。"
    exit 1
fi

# 创建输出目录
OUTPUT_DIR="processed_audio"
mkdir -p "$OUTPUT_DIR"

echo "🚀 开始批量优化音频文件..."

START_TIME=$(date +%s)

for file in *.m4a; do
    [ -e "$file" ] || continue
    echo "Processing $file..."
    # 使用轻量级滤镜替代 loudnorm
    # (Use lightweight filter instead of loudnorm)
    ffmpeg -i "$file" -af "volume=1.2,lowpass=f=4000" "processed_$file" -y -loglevel error
done

END_TIME=$(date +%s)
echo "Total processing time: $((END_TIME - START_TIME)) seconds."
# (总耗时: ... 秒)
echo "🎉 所有音频文件处理完毕，结果已存放至 $OUTPUT_DIR 文件夹。"