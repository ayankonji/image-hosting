# 快速参考卡片

## 📋 基本信息

- **仓库地址**: https://github.com/ayankonji/image-hosting
- **GitHub Pages**: https://ayankonji.github.io/image-hosting/
- **图片URL格式**: `https://ayankonji.github.io/image-hosting/images/<filename>`

## 🔧 环境变量配置

```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_USERNAME="ayankonji"
```

## 📤 上传图片

### Python脚本上传
```python
from scripts.upload import ImageUploader

uploader = ImageUploader()
url = uploader.upload_image("photo.jpg")
print(f"图片URL: {url}")
```

### 命令行上传
```bash
# 单张图片
python scripts/upload.py photo.jpg

# 批量上传
python scripts/batch_upload.py /path/to/images/
```

### Shell脚本上传
```bash
./scripts/upload.sh photo.jpg
```

## 📥 下载图片

```python
import requests

url = "https://ayankonji.github.io/image-hosting/images/photo.jpg"
response = requests.get(url)

if response.status_code == 200:
    with open("downloaded.jpg", "wb") as f:
        f.write(response.content)
```

## 🔗 URL管理

### 获取图片URL
```python
from scripts.config import get_image_url

url = get_image_url("photo.jpg")
# 返回: https://ayankonji.github.io/image-hosting/images/photo.jpg
```

### 批量URL管理
```python
from scripts.upload import ImageUploader

uploader = ImageUploader()

# 上传多张图片
urls = []
for image_path in image_list:
    url = uploader.upload_image(image_path)
    if url:
        urls.append(url)
```

## 🛠️ 调试命令

### 检查GitHub连接
```bash
gh auth status
```

### 检查仓库状态
```bash
gh repo view ayankonji/image-hosting
```

### 检查Pages部署
```bash
curl -I https://ayankonji.github.io/image-hosting/
```

### 查看上传历史
```bash
git log --oneline
```

## ⚠️ 常见问题

### 问题1：上传失败 (401)
**解决**: 检查GitHub Token是否正确

### 问题2：上传失败 (403)
**解决**: 检查Token权限，确保包含`repo`

### 问题3：图片URL返回404
**解决**: 等待几分钟让GitHub Pages部署完成

### 问题4：上传速度慢
**解决**: 检查网络连接，减少图片大小

## 📁 文件结构

```
image-hosting/
├── images/              # 图片存储
├── scripts/             # 上传脚本
│   ├── upload.py        # 单张上传
│   ├── batch_upload.py  # 批量上传
│   └── config.py        # 配置管理
├── docs/                # 文档
└── index.html           # GitHub Pages主页
```

## 🔐 安全提醒

1. **不要泄露Token**
2. **定期轮换Token**
3. **使用环境变量存储敏感信息**
4. **不要将Token提交到Git**

## 📞 获取帮助

- **项目文档**: https://github.com/ayankonji/image-hosting/tree/main/docs
- **GitHub Pages**: https://ayankonji.github.io/image-hosting/
- **GitHub API文档**: https://docs.github.com/rest

## 🚀 快速开始

1. 配置环境变量
2. 运行上传脚本
3. 获取图片URL
4. 在AI设备中使用URL

---

**💡 提示**: 图片URL是公开的，任何人都可以访问。请确保不上传敏感图片。