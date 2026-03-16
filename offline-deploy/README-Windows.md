# 离线部署指南（Windows 环境）

## 概述

由于服务器网络限制，无法直接访问 Docker Hub。本方案通过**本地打包镜像 → 上传到服务器 → 导入部署**的方式完成部署。

## 环境要求

- 本地电脑：Windows 11，已安装 Docker Desktop
- 服务器：Ubuntu 24.04，已安装 Docker
- 网络：本地电脑可以 SSH/SCP 连接服务器

---

## 步骤 1：本地打包镜像（Windows 11）

### 方式一：使用 PowerShell 脚本（推荐）

```powershell
# 1. 打开 PowerShell（管理员）
# 右键点击开始菜单 → Windows PowerShell (管理员)

# 2. 进入项目目录
cd E:\pyStudy\zulin\offline-deploy

# 3. 执行打包脚本
.\package-images.ps1
```

### 方式二：手动执行命令

```powershell
# 1. 拉取镜像
docker pull docker.io/library/nginx:alpine
docker pull docker.io/library/python:3.11-slim
docker pull docker.io/library/node:20-alpine

# 2. 保存为 tar 文件
docker save docker.io/library/nginx:alpine -o nginx-alpine.tar
docker save docker.io/library/python:3.11-slim -o python-3.11-slim.tar
docker save docker.io/library/node:20-alpine -o node-20-alpine.tar

# 3. 压缩（使用 7-Zip 或其他工具）
# 右键点击三个 tar 文件 → 7-Zip → 添加到压缩包
# 或使用 PowerShell 压缩
Compress-Archive -Path *.tar -DestinationPath docker-images.tar.gz -CompressionLevel Optimal
```

生成文件：`offline-deploy\docker-images.tar.gz`（约 300-500MB）

---

## 步骤 2：上传镜像到服务器

### 方式一：使用 WinSCP（推荐）

1. 下载安装 WinSCP：https://winscp.net/
2. 连接到服务器：
   - 主机名：`59.110.139.122`
   - 用户名：`root`
   - 密码：`你的密码`
3. 将 `docker-images.tar.gz` 拖拽到服务器 `/tmp/` 目录

### 方式二：使用 PowerShell SCP 命令

```powershell
# 在 PowerShell 中执行
$server = "59.110.139.122"
$user = "root"
$file = "E:\pyStudy\zulin\offline-deploy\docker-images.tar.gz"

# 使用 pscp (PuTTY 套件)
pscp $file $user@$server`:/tmp/

# 或使用 PowerShell 7 的 SCP 命令
scp $file $user@$server`:/tmp/
```

### 方式三：使用 Git Bash

```bash
# 在 Git Bash 中执行
scp /e/pyStudy/zulin/offline-deploy/docker-images.tar.gz root@59.110.139.122:/tmp/
```

---

## 步骤 3：服务器上导入镜像

### 3.1 登录服务器

```bash
# 使用 PowerShell
ssh root@59.110.139.122

# 或使用 PuTTY / Windows Terminal
```

### 3.2 导入镜像

```bash
cd /tmp
tar -xzf docker-images.tar.gz

docker load < nginx-alpine.tar
docker load < python-3.11-slim.tar
docker load < node-20-alpine.tar

# 验证镜像
docker images | grep -E "nginx|python|node"
```

---

## 步骤 4：部署应用

### 4.1 拉取项目代码

```bash
cd /data/www
git clone https://github.com/fcsx20241120/zulin.git
cd zulin
```

### 4.2 配置文件

```bash
# 复制环境配置
cp .env.example .env

# 编辑配置（MySQL 等）
vim .env
```

### 4.3 创建必要目录

```bash
mkdir -p out nginx/ssl
[ -f "ht.docx" ] && cp ht.docx out/
```

### 4.4 构建并启动

```bash
docker compose build
docker compose up -d
```

### 4.5 初始化数据库

```bash
docker compose exec backend python init_db.py
```

---

## 步骤 5：验证部署

### 5.1 查看服务状态

```bash
docker compose ps
```

### 5.2 查看日志

```bash
docker compose logs backend
docker compose logs frontend
docker compose logs nginx
```

### 5.3 测试访问

在浏览器中访问：
```
http://59.110.139.122:8088
```

---

## 快速部署脚本（服务器端）

在服务器上执行一键部署：

```bash
# 下载并执行部署脚本
cd /tmp
chmod +x /data/www/zulin/offline-deploy/deploy-on-server.sh
/data/www/zulin/offline-deploy/deploy-on-server.sh
```

---

## 常见问题

### Q1: Docker Desktop 无法启动

**解决方案：**
1. 确保已启用 Hyper-V 和容器功能
2. 在 BIOS 中启用虚拟化技术（VT-x/AMD-V）
3. 重启电脑

### Q2: 镜像保存失败

```powershell
# 检查 Docker 是否运行
docker ps

# 检查磁盘空间
docker system df

# 清理未使用的镜像
docker image prune -f
```

### Q3: 上传速度慢

- 使用 FTP 工具（FileZilla）断点续传
- 或使用压缩率更高的格式（.7z）
- 或分卷压缩后分别上传

### Q4: `docker load` 失败

```bash
# 检查文件是否完整
ls -lh /tmp/docker-images.tar.gz
md5sum /tmp/docker-images.tar.gz

# 重新解压
cd /tmp
rm -rf *.tar
tar -xzf docker-images.tar.gz
docker load < nginx-alpine.tar
```

---

## 文件结构

```
offline-deploy/
├── README.md              # 本文件
├── package-images.ps1     # Windows 打包脚本
├── deploy-on-server.sh    # 服务器部署脚本
└── docker-images.tar.gz   # 生成的镜像包
```

---

## 更新应用

后续更新时，只需上传代码和变更的镜像：

### 在 Windows 本地：

```powershell
# 1. 拉取最新代码
git pull origin main

# 2. 重新打包镜像（如有更新）
cd offline-deploy
.\package-images.ps1

# 3. 上传到服务器
scp docker-images.tar.gz root@59.110.139.122:/tmp/
```

### 在服务器上：

```bash
# 1. 拉取代码
cd /data/www/zulin
git pull origin main

# 2. 导入新镜像
cd /tmp
tar -xzf docker-images.tar.gz
docker load < nginx-alpine.tar  # 如有更新

# 3. 重新构建并启动
docker compose down
docker compose build
docker compose up -d
```

---

## 技术支持

遇到问题请查看：
- Docker Desktop 文档：https://docs.docker.com/desktop/
- PowerShell 文档：https://docs.microsoft.com/powershell/
