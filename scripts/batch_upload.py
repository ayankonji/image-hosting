#!/usr/bin/env python3
"""
批量上传脚本 - 用于嵌入式设备批量上传图片
使用方法：python batch_upload.py <directory_path>
"""

import os
import sys
import time
from pathlib import Path
from upload import upload_image_to_github

def batch_upload_images(directory_path):
    """
    批量上传目录中的所有图片
    
    Args:
        directory_path: 包含图片的目录路径
    
    Returns:
        list: 上传成功的图片URL列表
    """
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"❌ 目录不存在: {directory_path}")
        return []
    
    # 获取所有图片文件
    image_files = []
    for file in os.listdir(directory_path):
        if Path(file).suffix.lower() in image_extensions:
            image_files.append(os.path.join(directory_path, file))
    
    if not image_files:
        print(f"❌ 在目录中未找到图片文件: {directory_path}")
        print(f"支持的格式: {', '.join(image_extensions)}")
        return []
    
    print(f"📁 找到 {len(image_files)} 个图片文件")
    print(f"🚀 开始批量上传...")
    
    uploaded_urls = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n📤 上传进度: {i}/{len(image_files)}")
        print(f"📄 文件: {os.path.basename(image_path)}")
        
        # 上传图片
        url = upload_image_to_github(image_path)
        
        if url:
            uploaded_urls.append(url)
            print(f"✅ 上传成功")
        else:
            print(f"❌ 上传失败")
        
        # 添加延迟，避免API限制
        if i < len(image_files):
            time.sleep(1)
    
    return uploaded_urls

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python batch_upload.py <directory_path>")
        print("示例: python batch_upload.py ./my_images/")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    
    print(f"🖼️  图片批量上传工具")
    print(f"📁 目标目录: {directory_path}")
    print("=" * 50)
    
    # 批量上传
    urls = batch_upload_images(directory_path)
    
    # 显示结果
    print("\n" + "=" * 50)
    print(f"📊 上传统计:")
    print(f"✅ 成功上传: {len(urls)} 张图片")
    
    if urls:
        print(f"\n🔗 图片直链URL:")
        for i, url in enumerate(urls, 1):
            print(f"{i}. {url}")
        
        # 保存URL到文件
        url_file = os.path.join(directory_path, "uploaded_urls.txt")
        with open(url_file, 'w') as f:
            f.write("# 上传成功的图片URL\n")
            f.write(f"# 上传时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for url in urls:
                f.write(f"{url}\n")
        
        print(f"\n💾 URL已保存到: {url_file}")
        print(f"📱 嵌入式设备可以读取此文件获取所有图片URL")
    
    print(f"\n🎉 批量上传完成!")

if __name__ == '__main__':
    main()