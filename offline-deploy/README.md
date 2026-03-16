# 离线部署指南

## 概述

由于服务器网络限制，无法直接访问 Docker Hub。本方案通过**本地打包镜像 → 上传到服务器 → 导入部署**的方式完成部署。

## 环境要求

- 本地电脑：可以正常访问 Docker Hub
- 服务器：Ubuntu 24.04，已安装 Docker
- 网络：本地电脑可以 SSH/SCP 连接服务器

---

## 步骤 1：本地打包镜像

### 1.1 创建打包脚本

在项目根目录创建 `offline-deploy/` 文件夹：

```bash
mkdir -p offline-deploy
```

### 1.2 执行打包脚本

```bash
# 在本地电脑执行
cd /path/to/zulin/offline-deploy
chmod +x package-images.sh
./package-images.sh
```

这将生成 `docker-images.tar.gz` 文件（约 300-500MB）。

---

## 步骤 2：上传镜像到服务器

### 2.1 使用 SCP 上传

```bash
# 在本地电脑执行
scp offline-deploy/docker-images.tar.gz root@59.110.139.122:/tmp/
```

### 2.2 或使用 FTP/SFTP 工具

- FileZilla
- WinSCP
- Xftp

上传到服务器 `/tmp/` 目录。

---

## 步骤 3：服务器上导入镜像

### 3.1 登录服务器

```bash
ssh root@59.110.139.122
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

```bash
# 在服务器上测试
curl http://localhost:8088

# 或在浏览器访问
http://59.110.139.122:8088
```

---

## 常见问题

### Q1: `docker load` 失败

```bash
# 检查 tar 文件是否完整
ls -lh /tmp/docker-images.tar.gz
tar -tzf docker-images.tar.gz | head -20
```

### Q2: 镜像导入后无法使用

```bash
# 检查镜像列表
docker images

# 重新标记镜像
docker tag nginx:alpine docker.io/library/nginx:alpine
```

### Q3: 构建失败

```bash
# 清理旧镜像
docker compose down
docker image prune -f

# 重新构建
docker compose build --no-cache
```

---

## 更新应用

后续更新时，只需上传代码和变更的镜像：

```bash
# 1. 在本地拉取最新代码
git pull origin main

# 2. 如果有新的基础镜像版本，重新打包
cd offline-deploy
./package-images.sh

# 3. 上传到服务器
scp docker-images.tar.gz root@59.110.139.122:/tmp/

# 4. 在服务器上更新
ssh root@59.110.139.122
cd /data/www/zulin
git pull origin main
docker compose down
docker load < /tmp/nginx-alpine.tar  # 如有更新
docker compose build
docker compose up -d
```

---

## 备份建议

```bash
# 定期备份数据库
mysqldump -h 59.110.139.122 -u root -p zulin > /backup/zulin_$(date +%Y%m%d).sql

# 备份 out 目录
tar -czf /backup/out_$(date +%Y%m%d).tar.gz /data/www/zulin/out/
```
