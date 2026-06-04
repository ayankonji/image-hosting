#!/usr/bin/env python3
"""
配置管理脚本 - 用于加载和管理上传配置
"""

import os
import json
from pathlib import Path

# 默认配置
DEFAULT_CONFIG = {
    "github": {
        "token": os.environ.get('GITHUB_TOKEN', ''),
        "username": os.environ.get('GITHUB_USERNAME', ''),
        "repo": "image-hosting",
        "branch": "main"
    },
    "upload": {
        "max_file_size_mb": 10,
        "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
        "auto_rename": True,
        "prefix": "img"
    },
    "urls": {
        "base_url": "https://{username}.github.io/{repo}/images",
        "format": "https://{username}.github.io/{repo}/images/{filename}"
    }
}

def load_config(config_path=None):
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径（可选）
    
    Returns:
        dict: 配置字典
    """
    config = DEFAULT_CONFIG.copy()
    
    # 尝试从配置文件加载
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"⚠️  无法加载配置文件: {e}")
    
    # 从环境变量加载
    if os.environ.get('GITHUB_TOKEN'):
        config['github']['token'] = os.environ['GITHUB_TOKEN']
    
    if os.environ.get('GITHUB_USERNAME'):
        config['github']['username'] = os.environ['GITHUB_USERNAME']
    
    return config

def save_config(config, config_path):
    """
    保存配置到文件
    
    Args:
        config: 配置字典
        config_path: 配置文件路径
    """
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置已保存到: {config_path}")
    except Exception as e:
        print(f"❌ 保存配置失败: {e}")

def get_image_url(filename, config=None):
    """
    生成图片URL
    
    Args:
        filename: 图片文件名
        config: 配置字典（可选）
    
    Returns:
        str: 图片URL
    """
    if config is None:
        config = load_config()
    
    username = config['github']['username']
    repo = config['github']['repo']
    
    return config['urls']['format'].format(
        username=username,
        repo=repo,
        filename=filename
    )

def main():
    """测试配置加载"""
    config = load_config()
    
    print("📋 当前配置:")
    print(f"GitHub用户名: {config['github']['username']}")
    print(f"仓库名: {config['github']['repo']}")
    print(f"分支: {config['github']['branch']}")
    print(f"最大文件大小: {config['upload']['max_file_size_mb']}MB")
    print(f"允许的扩展名: {', '.join(config['upload']['allowed_extensions'])}")
    
    # 测试URL生成
    test_filename = "test_image.jpg"
    url = get_image_url(test_filename, config)
    print(f"\n🔗 测试URL: {url}")

if __name__ == '__main__':
    main()