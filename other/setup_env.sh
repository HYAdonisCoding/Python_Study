#!/bin/bash

echo "🚀 创建虚拟环境..."

PYTHON_PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
ENV_PATH="$HOME/envs/py_arm64"

# 删除旧环境
rm -rf $ENV_PATH

# 创建新环境
$PYTHON_PATH -m venv $ENV_PATH

# 激活环境
source $ENV_PATH/bin/activate

echo "📦 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 环境搭建完成！"