#!/usr/bin/env python3
"""
图片上传脚本 - 用于嵌入式设备上传图片到GitHub Pages
使用方法：python upload.py <image_path> [custom_filename]
"""

import os
import sys
import base64
import json
import requests
from pathlib import Path
import mimetypes

# 配置信息
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', 'your_github_token_here')
REPO_OWNER = os.environ.get('GITHUB_USERNAME', 'your_username')
REPO_NAME = 'image-hosting'
BRANCH = 'main'

def get_github_headers():
    """获取GitHub API请求头"""
    return {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }

def upload_image_to_github(image_path, custom_filename=None):
    """
    上传图片到GitHub仓库
    
    Args:
        image_path: 图片文件路径
        custom_filename: 自定义文件名（可选）
    
    Returns:
        str: 图片的直链URL
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 获取文件名
        if custom_filename:
            filename = custom_filename
        else:
            filename = os.path.basename(image_path)
        
        # 确保文件名是英文和数字
        filename = "".join(c for c in filename if c.isalnum() or c in '.-_').strip()
        if not filename:
            filename = f"image_{int(time.time())}.jpg"
        
        # 读取图片文件
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # 编码为base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # GitHub API端点
        api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/images/{filename}"
        
        # 检查文件是否已存在
        response = requests.get(api_url, headers=get_github_headers())
        
        if response.status_code == 200:
            # 文件已存在，需要更新
            file_sha = response.json()['sha']
            data = {
                'message': f'Update image: {filename}',
                'content': image_base64,
                'sha': file_sha,
                'branch': BRANCH
            }
        else:
            # 文件不存在，创建新文件
            data = {
                'message': f'Upload image: {filename}',
                'content': image_base64,
                'branch': BRANCH
            }
        
        # 上传图片
        response = requests.put(api_url, headers=get_github_headers(), json=data)
        
        if response.status_code in [200, 201]:
            # 生成直链URL
            image_url = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/images/{filename}"
            print(f"✅ 图片上传成功!")
            print(f"📁 文件名: {filename}")
            print(f"🔗 直链URL: {image_url}")
            return image_url
        else:
            print(f"❌ 上传失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 上传出错: {str(e)}")
        return None

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python upload.py <image_path> [custom_filename]")
        print("示例: python upload.py photo.jpg my_photo.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    custom_filename = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 上传图片
    url = upload_image_to_github(image_path, custom_filename)
    
    if url:
        print(f"\n🎉 图片已成功上传!")
        print(f"📱 嵌入式设备可以访问此URL获取图片")
        print(f"💡 提示: 将此URL保存到您的设备配置中")

if __name__ == '__main__':
    import time
    main()