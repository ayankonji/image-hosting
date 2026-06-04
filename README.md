# Image Hosting for AI Devices

这是一个专为AI驱动的嵌入式设备设计的图片托管仓库。通过GitHub Pages提供图片直链URL，方便设备上传和访问图片。

## 功能特点

- 🖼️ 图片直链URL访问
- 🤖 嵌入式设备友好
- 🚀 GitHub Pages自动部署
- 📁 简单的图片管理
- 🔗 即插即用的API接口

## 快速开始

### 1. 上传图片

使用提供的上传脚本：

```bash
# 上传单张图片
./scripts/upload.sh /path/to/image.jpg

# 批量上传图片
./scripts/batch_upload.sh /path/to/images/
```

### 2. 获取直链URL

上传后，图片将可通过以下格式的URL访问：

```
https://ayankonji.github.io/image-hosting/images/<filename>
```

### 3. 嵌入式设备集成

在您的AI设备中使用以下代码示例：

```python
import requests

# 上传图片
def upload_image(image_path):
    # 使用GitHub API上传
    pass

# 获取图片URL
def get_image_url(filename):
    return f"https://ayankonji.github.io/image-hosting/images/{filename}"
```

## 目录结构

```
image-hosting/
├── images/          # 图片存储目录
├── scripts/         # 上传和管理脚本
├── docs/            # 文档
├── .github/         # GitHub Actions配置
└── README.md        # 本文件
```

## 使用场景

- AI摄像头图片存储
- 嵌入式设备图片上传
- 物联网设备图片共享
- 机器学习数据集托管

## 注意事项

- 图片文件名请使用英文和数字
- 建议图片大小不超过10MB
- 支持常见图片格式：JPG、PNG、GIF、WebP

## 许可证

MIT License