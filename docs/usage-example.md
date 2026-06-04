# 嵌入式设备使用示例

## 1. Python设备集成

### 基本上传示例

```python
import requests
import base64
import os

# 配置信息
GITHUB_TOKEN = "your_github_token"
USERNAME = "your_username"
REPO = "image-hosting"

def upload_image(image_path):
    """上传图片到GitHub"""
    # 读取图片
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 编码为base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    filename = os.path.basename(image_path)
    
    # GitHub API
    url = f"https://api.github.com/repos/{USERNAME}/{REPO}/contents/images/{filename}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'message': f'Upload image: {filename}',
        'content': image_base64
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 201:
        # 返回直链URL
        image_url = f"https://{USERNAME}.github.io/{REPO}/images/{filename}"
        return image_url
    else:
        print(f"上传失败: {response.status_code}")
        return None

# 使用示例
if __name__ == '__main__':
    image_path = "photo.jpg"
    url = upload_image(image_path)
    if url:
        print(f"图片URL: {url}")
```

### 图片下载和处理

```python
import requests
from PIL import Image
import io

def download_and_process_image(image_url):
    """下载并处理图片"""
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # 将图片数据转换为PIL Image
        image = Image.open(io.BytesIO(response.content))
        
        # 处理图片（示例：调整大小）
        image = image.resize((800, 600))
        
        # 保存或进一步处理
        image.save("processed_image.jpg")
        print("图片处理完成")
        return True
    else:
        print(f"下载失败: {response.status_code}")
        return False

# 使用示例
image_url = "https://username.github.io/image-hosting/images/photo.jpg"
download_and_process_image(image_url)
```

## 2. Arduino/ESP32集成

### ESP32上传示例

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "your_wifi_ssid";
const char* password = "your_wifi_password";
const char* githubToken = "your_github_token";
const char* username = "your_username";
const char* repo = "image-hosting";

String uploadImage(uint8_t* imageData, size_t imageSize, String filename) {
    HTTPClient http;
    
    // 构建API URL
    String url = "https://api.github.com/repos/" + String(username) + "/" + String(repo) + "/contents/images/" + filename;
    
    http.begin(url);
    http.addHeader("Authorization", "token " + String(githubToken));
    http.addHeader("Accept", "application/vnd.github.v3+json");
    http.addHeader("Content-Type", "application/json");
    
    // Base64编码
    String base64Image = base64::encode(imageData, imageSize);
    
    // 构建JSON请求
    StaticJsonDocument<1024> doc;
    doc["message"] = "Upload image from ESP32";
    doc["content"] = base64Image;
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.PUT(jsonString);
    
    if (httpResponseCode == 201) {
        // 返回直链URL
        String imageUrl = "https://" + String(username) + ".github.io/" + String(repo) + "/images/" + filename;
        http.end();
        return imageUrl;
    } else {
        Serial.println("Upload failed: " + String(httpResponseCode));
        http.end();
        return "";
    }
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    
    Serial.println("Connected to WiFi");
    
    // 示例：上传图片
    // uint8_t imageData[] = {...}; // 图片数据
    // String url = uploadImage(imageData, sizeof(imageData), "esp32_photo.jpg");
    // Serial.println("Image URL: " + url);
}

void loop() {
    // 主循环
}
```

## 3. 树莓派集成

### 树莓派摄像头上传

```python
import picamera
import time
import requests
import base64
import os

def capture_and_upload():
    """拍摄照片并上传"""
    with picamera.PiCamera() as camera:
        # 设置摄像头
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(2)  # 等待摄像头稳定
        
        # 拍摄照片
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"raspi_{timestamp}.jpg"
        camera.capture(filename)
        camera.stop_preview()
        
        print(f"照片已保存: {filename}")
        
        # 上传照片
        url = upload_image(filename)
        if url:
            print(f"照片URL: {url}")
            return url
        return None

def upload_image(image_path):
    """上传图片到GitHub"""
    # 这里使用之前定义的upload_image函数
    # 实际使用时需要配置GitHub Token和用户名
    pass

if __name__ == '__main__':
    capture_and_upload()
```

## 4. 批量上传脚本

### 定时批量上传

```python
import os
import time
from datetime import datetime
from batch_upload import batch_upload_images

def scheduled_upload():
    """定时批量上传"""
    image_dir = "/path/to/images"
    
    print(f"开始定时上传任务: {datetime.now()}")
    
    # 批量上传
    urls = batch_upload_images(image_dir)
    
    if urls:
        print(f"成功上传 {len(urls)} 张图片")
        
        # 记录上传历史
        with open("upload_history.log", "a") as f:
            f.write(f"{datetime.now()}: 上传 {len(urls)} 张图片\n")
    
    return urls

# 每小时执行一次
while True:
    scheduled_upload()
    time.sleep(3600)  # 3600秒 = 1小时
```

## 5. 错误处理和重试机制

### 带重试的上传函数

```python
import time
import requests
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"尝试 {attempt + 1} 失败: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=2)
def upload_with_retry(image_path):
    """带重试的上传函数"""
    # 这里是上传逻辑
    pass
```

## 6. 图片URL管理

### URL存储和检索

```python
import json
import os

class ImageURLManager:
    """图片URL管理器"""
    
    def __init__(self, storage_file="image_urls.json"):
        self.storage_file = storage_file
        self.urls = self.load_urls()
    
    def load_urls(self):
        """加载URL存储"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_urls(self):
        """保存URL存储"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.urls, f, indent=2)
    
    def add_url(self, image_name, url, metadata=None):
        """添加URL"""
        self.urls[image_name] = {
            'url': url,
            'uploaded_at': time.time(),
            'metadata': metadata or {}
        }
        self.save_urls()
    
    def get_url(self, image_name):
        """获取URL"""
        return self.urls.get(image_name, {}).get('url')
    
    def list_images(self):
        """列出所有图片"""
        return list(self.urls.keys())

# 使用示例
manager = ImageURLManager()
manager.add_url("photo1.jpg", "https://username.github.io/image-hosting/images/photo1.jpg")
url = manager.get_url("photo1.jpg")
print(f"图片URL: {url}")
```

## 7. 集成到AI处理流程

### AI设备图片处理流程

```python
import requests
import cv2
import numpy as np
from PIL import Image
import io

class AIImageProcessor:
    """AI图片处理器"""
    
    def __init__(self, image_url):
        self.image_url = image_url
        self.image = None
    
    def download_image(self):
        """下载图片"""
        response = requests.get(self.image_url)
        if response.status_code == 200:
            # 转换为OpenCV格式
            image_array = np.frombuffer(response.content, dtype=np.uint8)
            self.image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return True
        return False
    
    def process_image(self):
        """处理图片"""
        if self.image is None:
            return None
        
        # 示例处理：灰度化
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # 示例处理：边缘检测
        edges = cv2.Canny(gray, 100, 200)
        
        return edges
    
    def save_result(self, filename):
        """保存处理结果"""
        if self.image is not None:
            cv2.imwrite(filename, self.image)
            return True
        return False

# 使用示例
processor = AIImageProcessor("https://username.github.io/image-hosting/images/photo.jpg")
if processor.download_image():
    result = processor.process_image()
    if result is not None:
        processor.save_result("processed.jpg")
        print("图片处理完成")
```

## 8. 部署建议

### 生产环境配置

1. **环境变量配置**
   ```bash
   export GITHUB_TOKEN="your_github_token"
   export GITHUB_USERNAME="your_username"
   ```

2. **定时任务**
   ```bash
   # 每小时批量上传
   0 * * * * /path/to/batch_upload.py /path/to/images/
   ```

3. **日志记录**
   ```python
   import logging
   logging.basicConfig(filename='image_upload.log', level=logging.INFO)
   ```

4. **监控脚本**
   ```python
   def monitor_uploads():
       """监控上传状态"""
       # 检查上传历史
       # 发送告警通知
       pass
   ```

这些示例展示了如何在各种嵌入式设备中集成图片上传和访问功能。根据您的具体设备和技术栈，可以选择适合的示例进行集成。