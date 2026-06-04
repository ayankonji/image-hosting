# 嵌入式设备图片访问集成指南

## 概述

本指南将帮助您将AI驱动的嵌入式设备连接到GitHub Pages图片托管服务，实现图片的上传和访问。

## 前提条件

1. **GitHub账户**：您需要有一个GitHub账户
2. **GitHub Token**：需要创建个人访问令牌用于上传图片
3. **网络连接**：嵌入式设备需要能够访问互联网
4. **Python环境**：设备需要安装Python 3.6+

## 第一步：配置GitHub Token

### 1.1 创建GitHub Token

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token"
3. 设置权限：
   - ✅ `repo` - 完整仓库访问权限
   - ✅ `workflow` - 更新GitHub Actions工作流
4. 生成并保存token

### 1.2 在设备上设置环境变量

```bash
# Linux/macOS
export GITHUB_TOKEN="your_github_token_here"
export GITHUB_USERNAME="ayankonji"

# Windows
set GITHUB_TOKEN=your_github_token_here
set GITHUB_USERNAME=ayankonji
```

## 第二步：设备端集成

### 2.1 Python设备集成

#### 基本上传脚本

```python
#!/usr/bin/env python3
"""
嵌入式设备图片上传客户端
"""

import os
import sys
import base64
import requests
import json
from datetime import datetime

class ImageUploader:
    def __init__(self, token=None, username=None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.username = username or os.environ.get('GITHUB_USERNAME', 'ayankonji')
        self.repo = 'image-hosting'
        self.branch = 'main'
        
        if not self.token:
            raise ValueError("GitHub token未设置")
    
    def get_headers(self):
        return {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
    
    def upload_image(self, image_path, custom_filename=None):
        """
        上传图片并返回直链URL
        
        Args:
            image_path: 图片文件路径
            custom_filename: 自定义文件名（可选）
        
        Returns:
            str: 图片URL，失败返回None
        """
        try:
            # 检查文件
            if not os.path.exists(image_path):
                print(f"❌ 文件不存在: {image_path}")
                return None
            
            # 获取文件名
            if custom_filename:
                filename = custom_filename
            else:
                # 生成带时间戳的文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = os.path.splitext(image_path)[1]
                filename = f"img_{timestamp}{ext}"
            
            # 清理文件名
            filename = "".join(c for c in filename if c.isalnum() or c in '.-_').strip()
            
            # 读取并编码图片
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # GitHub API
            api_url = f"https://api.github.com/repos/{self.username}/{self.repo}/contents/images/{filename}"
            
            # 检查文件是否存在
            response = requests.get(api_url, headers=self.get_headers())
            
            if response.status_code == 200:
                # 更新现有文件
                file_sha = response.json()['sha']
                data = {
                    'message': f'Update image: {filename}',
                    'content': image_base64,
                    'sha': file_sha,
                    'branch': self.branch
                }
            else:
                # 创建新文件
                data = {
                    'message': f'Upload image: {filename}',
                    'content': image_base64,
                    'branch': self.branch
                }
            
            # 上传
            response = requests.put(api_url, headers=self.get_headers(), json=data)
            
            if response.status_code in [200, 201]:
                image_url = f"https://{self.username}.github.io/{self.repo}/images/{filename}"
                print(f"✅ 上传成功: {filename}")
                print(f"🔗 URL: {image_url}")
                return image_url
            else:
                print(f"❌ 上传失败: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            return None
    
    def get_image_url(self, filename):
        """获取图片URL"""
        return f"https://{self.username}.github.io/{self.repo}/images/{filename}"

# 使用示例
if __name__ == '__main__':
    uploader = ImageUploader()
    
    # 上传图片
    image_path = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
    url = uploader.upload_image(image_path)
    
    if url:
        print(f"\n🎉 图片URL: {url}")
        print("📱 AI设备可以使用此URL访问图片")
```

#### 图片下载和处理

```python
import requests
from PIL import Image
import io

def download_image(url):
    """下载图片"""
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    return None

def process_image_for_ai(image_url):
    """处理图片供AI分析"""
    image = download_image(image_url)
    if image:
        # 调整大小
        image = image.resize((224, 224))
        
        # 转换为numpy数组
        import numpy as np
        image_array = np.array(image)
        
        # 归一化
        image_array = image_array / 255.0
        
        return image_array
    return None

# AI处理流程
image_url = "https://ayankonji.github.io/image-hosting/images/photo.jpg"
processed_image = process_image_for_ai(image_url)
if processed_image is not None:
    print("图片已处理，可以输入AI模型")
```

### 2.2 ESP32/Arduino集成

#### ESP32代码示例

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <base64.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* githubToken = "YOUR_GITHUB_TOKEN";
const char* username = "ayankonji";
const char* repo = "image-hosting";

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("连接WiFi中...");
    }
    Serial.println("WiFi已连接");
}

String uploadImage(uint8_t* imageData, size_t imageSize, String filename) {
    HTTPClient http;
    
    String url = "https://api.github.com/repos/" + String(username) + "/" + String(repo) + "/contents/images/" + filename;
    
    http.begin(url);
    http.addHeader("Authorization", "token " + String(githubToken));
    http.addHeader("Accept", "application/vnd.github.v3+json");
    http.addHeader("Content-Type", "application/json");
    
    // Base64编码
    String base64Image = base64::encode(imageData, imageSize);
    
    // 构建JSON
    StaticJsonDocument<1024> doc;
    doc["message"] = "Upload from ESP32";
    doc["content"] = base64Image;
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.PUT(jsonString);
    
    if (httpResponseCode == 201) {
        String imageUrl = "https://" + String(username) + ".github.io/" + String(repo) + "/images/" + filename;
        http.end();
        return imageUrl;
    } else {
        Serial.println("上传失败: " + String(httpResponseCode));
        http.end();
        return "";
    }
}

void loop() {
    // 拍摄照片并上传
    // camera_fb_t * fb = esp_camera_fb_get();
    // String url = uploadImage(fb->buf, fb->len, "esp32_photo.jpg");
    // Serial.println("图片URL: " + url);
    
    delay(60000); // 每分钟上传一次
}
```

### 2.3 树莓派集成

#### 树莓派摄像头上传

```python
#!/usr/bin/env python3
"""
树莓派摄像头图片上传
"""

import picamera
import time
import sys
sys.path.append('/path/to/scripts')
from upload import ImageUploader

def capture_and_upload():
    """拍摄并上传照片"""
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(2)
        
        # 生成文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"raspi_{timestamp}.jpg"
        
        # 拍摄照片
        camera.capture(filename)
        camera.stop_preview()
        
        print(f"📸 照片已拍摄: {filename}")
        
        # 上传照片
        uploader = ImageUploader()
        url = uploader.upload_image(filename)
        
        if url:
            print(f"🔗 照片URL: {url}")
            
            # 保存URL到文件
            with open("photo_urls.txt", "a") as f:
                f.write(f"{timestamp}: {url}\n")
            
            return url
        return None

if __name__ == '__main__':
    capture_and_upload()
```

## 第三步：AI设备访问图片

### 3.1 直接URL访问

您的AI设备可以直接通过URL访问图片：

```
https://ayankonji.github.io/image-hosting/images/<filename>
```

### 3.2 Python下载示例

```python
import requests

def download_image_from_url(url, save_path=None):
    """从URL下载图片"""
    response = requests.get(url)
    
    if response.status_code == 200:
        if save_path:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ 图片已保存到: {save_path}")
        return response.content
    else:
        print(f"❌ 下载失败: {response.status_code}")
        return None

# 使用示例
url = "https://ayankonji.github.io/image-hosting/images/photo.jpg"
image_data = download_image_from_url(url, "downloaded_photo.jpg")
```

### 3.3 批量图片管理

```python
import json
import os

class ImageManager:
    """图片管理器"""
    
    def __init__(self, storage_file="images.json"):
        self.storage_file = storage_file
        self.images = self.load_images()
    
    def load_images(self):
        """加载图片列表"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_images(self):
        """保存图片列表"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.images, f, indent=2)
    
    def add_image(self, name, url, metadata=None):
        """添加图片记录"""
        self.images[name] = {
            'url': url,
            'uploaded_at': time.time(),
            'metadata': metadata or {}
        }
        self.save_images()
    
    def get_image_url(self, name):
        """获取图片URL"""
        return self.images.get(name, {}).get('url')
    
    def list_images(self):
        """列出所有图片"""
        return list(self.images.keys())

# 使用示例
manager = ImageManager()
manager.add_image("photo1", "https://ayankonji.github.io/image-hosting/images/photo1.jpg")
url = manager.get_image_url("photo1")
```

## 第四步：自动化工作流

### 4.1 定时上传脚本

```python
#!/usr/bin/env python3
"""
定时图片上传脚本
"""

import time
import os
from datetime import datetime
from upload import ImageUploader

def scheduled_upload(image_dir, interval_seconds=3600):
    """定时上传任务"""
    uploader = ImageUploader()
    
    print(f"⏰ 定时上传任务启动")
    print(f"📁 监控目录: {image_dir}")
    print(f"⏱️  上传间隔: {interval_seconds}秒")
    
    while True:
        print(f"\n🕐 {datetime.now()} - 开始上传任务")
        
        # 获取目录中的图片
        image_files = []
        for file in os.listdir(image_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_files.append(os.path.join(image_dir, file))
        
        if image_files:
            print(f"📸 找到 {len(image_files)} 张图片")
            
            for image_path in image_files:
                url = uploader.upload_image(image_path)
                if url:
                    print(f"✅ 上传成功: {os.path.basename(image_path)}")
                time.sleep(1)  # 避免API限制
        else:
            print("📭 没有找到新图片")
        
        print(f"⏳ 等待 {interval_seconds} 秒...")
        time.sleep(interval_seconds)

if __name__ == '__main__':
    scheduled_upload("/path/to/images", 3600)
```

### 4.2 系统服务配置

#### Linux systemd服务

```ini
# /etc/systemd/system/image-uploader.service
[Unit]
Description=Image Upload Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/image-uploader
Environment=GITHUB_TOKEN=your_token_here
Environment=GITHUB_USERNAME=ayankonji
ExecStart=/usr/bin/python3 /home/pi/image-uploader/scheduled_upload.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl enable image-uploader
sudo systemctl start image-uploader
```

## 第五步：故障排除

### 5.1 常见问题

#### 问题1：上传失败，返回401错误
**原因**：GitHub Token无效或过期
**解决**：
1. 检查Token是否正确
2. 确认Token权限包含`repo`
3. 重新生成Token

#### 问题2：上传失败，返回403错误
**原因**：API速率限制
**解决**：
1. 减少上传频率
2. 添加延迟（1-2秒）
3. 使用认证请求（已认证用户限制更高）

#### 问题3：图片URL无法访问
**原因**：GitHub Pages未部署或部署失败
**解决**：
1. 检查仓库Settings → Pages
2. 确认源分支设置为`main`
3. 等待几分钟让部署完成

#### 问题4：图片上传后URL返回404
**原因**：GitHub Pages缓存
**解决**：
1. 等待几分钟
2. 强制刷新浏览器缓存
3. 检查文件名是否正确

### 5.2 调试脚本

```python
#!/usr/bin/env python3
"""
调试脚本 - 检查配置和连接
"""

import os
import requests

def debug_check():
    """调试检查"""
    print("🔍 调试检查开始\n")
    
    # 检查环境变量
    token = os.environ.get('GITHUB_TOKEN')
    username = os.environ.get('GITHUB_USERNAME', 'ayankonji')
    
    print(f"GitHub Token: {'✅ 已设置' if token else '❌ 未设置'}")
    print(f"GitHub 用户名: {username}")
    
    if token:
        # 测试API连接
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"GitHub 连接: ✅ 成功")
            print(f"用户: {user_data['login']}")
        else:
            print(f"GitHub 连接: ❌ 失败 ({response.status_code})")
    
    # 测试Pages访问
    pages_url = f"https://{username}.github.io/image-hosting/"
    response = requests.get(pages_url)
    
    print(f"\nGitHub Pages 状态: {'✅ 可访问' if response.status_code == 200 else '❌ 不可访问'}")
    print(f"Pages URL: {pages_url}")
    
    print("\n🔍 调试检查完成")

if __name__ == '__main__':
    debug_check()
```

## 第六步：最佳实践

### 6.1 安全建议

1. **Token安全**
   - 不要将Token硬编码在代码中
   - 使用环境变量存储Token
   - 定期轮换Token

2. **文件命名**
   - 使用有意义的文件名
   - 包含时间戳避免冲突
   - 避免特殊字符

3. **错误处理**
   - 添加重试机制
   - 记录错误日志
   - 实现优雅降级

### 6.2 性能优化

1. **批量上传**
   - 合并多个小文件
   - 使用压缩减少大小
   - 实现并行上传

2. **缓存策略**
   - 缓存已上传的URL
   - 避免重复上传
   - 实现增量更新

3. **网络优化**
   - 使用连接池
   - 实现超时重试
   - 监控网络状态

## 示例场景

### 场景1：AI摄像头监控

```python
import cv2
import time
from upload import ImageUploader

def monitor_and_upload():
    """监控摄像头并上传截图"""
    cap = cv2.VideoCapture(0)
    uploader = ImageUploader()
    
    while True:
        ret, frame = cap.read()
        if ret:
            # 保存截图
            filename = f"monitor_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            
            # 上传截图
            url = uploader.upload_image(filename)
            if url:
                print(f"📸 监控截图已上传: {url}")
            
            # 清理本地文件
            os.remove(filename)
        
        time.sleep(60)  # 每分钟上传一次

monitor_and_upload()
```

### 场景2：物联网传感器数据可视化

```python
import matplotlib.pyplot as plt
import numpy as np
from upload import ImageUploader

def create_sensor_chart(sensor_data):
    """创建传感器数据图表"""
    plt.figure(figsize=(10, 6))
    plt.plot(sensor_data)
    plt.title('Sensor Data')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    
    # 保存图表
    filename = "sensor_chart.png"
    plt.savefig(filename)
    plt.close()
    
    # 上传图表
    uploader = ImageUploader()
    url = uploader.upload_image(filename)
    
    return url

# 使用示例
data = np.random.randn(100)
chart_url = create_sensor_chart(data)
print(f"📊 图表URL: {chart_url}")
```

## 总结

通过本指南，您已经学会了：

1. ✅ 配置GitHub Token和环境
2. ✅ 在嵌入式设备上集成图片上传
3. ✅ 通过URL访问图片
4. ✅ 实现自动化工作流
5. ✅ 处理常见问题

您的AI设备现在可以：
- 📸 上传图片到GitHub Pages
- 🔗 获取图片直链URL
- 🤖 通过URL访问和分析图片
- 📊 管理图片库

## 获取帮助

如有问题，请参考：
- GitHub Pages文档：https://docs.github.com/pages
- GitHub API文档：https://docs.github.com/rest
- 项目README：https://github.com/ayankonji/image-hosting

---

**🎉 恭喜！您的AI设备图片托管系统已准备就绪！**