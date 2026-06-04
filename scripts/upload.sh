#!/bin/bash

# 图片上传脚本 - Shell版本
# 使用方法: ./upload.sh <image_path> [custom_filename]

set -e

# 检查参数
if [ $# -lt 1 ]; then
    echo "使用方法: ./upload.sh <image_path> [custom_filename]"
    echo "示例: ./upload.sh photo.jpg my_photo.jpg"
    exit 1
fi

IMAGE_PATH="$1"
CUSTOM_FILENAME="$2"

# 检查文件是否存在
if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ 图片文件不存在: $IMAGE_PATH"
    exit 1
fi

# 检查是否安装了Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装Python3"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 运行Python上传脚本
echo "🚀 开始上传图片..."
python3 "$SCRIPT_DIR/upload.py" "$IMAGE_PATH" "$CUSTOM_FILENAME"

echo "🎉 上传完成!"