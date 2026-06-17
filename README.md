# ESP-Claw Image Hosting

一个兼容 ESP-Skill 格式的图片托管仓库。

## 目录结构

- `images/` — 托管的图片文件
- `skills/` — ESP-Claw 技能

## 使用方式

### 上传图片

通过 ESP-Claw 的 `image_hosting` 技能上传图片，需要提供 GitHub Personal Access Token。

### 直接访问图片

上传后的图片可通过以下格式访问：
```
https://raw.githubusercontent.com/ayankonji/image-hosting/main/images/<filename>
```

## Token 说明

本仓库不存储任何 token。使用前请自行生成 GitHub PAT（需要 `repo` 权限），并在调用技能时提供。
