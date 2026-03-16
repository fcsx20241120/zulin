# Docker Compose 部署指南

## 前置要求

- Ubuntu 24.04 LTS
- Docker 20.10+
- Docker Compose 2.0+

## 快速开始

### 1. 安装 Docker

```bash
# 添加 Docker 官方 GPG 密钥
sudo apt update
sudo apt install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 添加 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 启动 Docker
sudo systemctl enable docker
sudo systemctl start docker

# 添加当前用户到 docker 组（可选，避免每次使用 sudo）
sudo usermod -aG docker $USER
```

### 2. 部署应用

```bash
# 克隆项目
git clone https://github.com/fcsx20241120/zulin.git
cd zulin

# 复制配置文件
cp .env.example .env

# 修改配置（可选）
vim .env

# 执行部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 3. 初始化数据库

```bash
# 进入后端容器
docker-compose exec backend bash

# 初始化数据库
python init_db.py

# 退出容器
exit
```

### 4. 访问应用

- 前端：http://your-server-ip
- 后端 API: http://your-server-ip/api/
- MySQL: localhost:3306

## 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 重启单个服务
docker-compose restart backend

# 停止服务
docker-compose down

# 停止并清理数据
docker-compose down -v

# 重新构建并启动
docker-compose up -d --build

# 进入容器
docker-compose exec backend bash
docker-compose exec mysql mysql -u zulin -p
```

## 配置说明

### .env 文件

| 变量 | 说明 | 默认值 |
|---|---|---|
| MYSQL_ROOT_PASSWORD | MySQL root 密码 | Zulin@2026! |
| MYSQL_DATABASE | 数据库名 | zulin |
| MYSQL_USER | 数据库用户 | zulin |
| MYSQL_PASSWORD | 数据库密码 | Zulin@2026! |
| SECRET_KEY | JWT 密钥 | 请修改为随机字符串 |
| HTTP_PORT | HTTP 端口 | 80 |
| HTTPS_PORT | HTTPS 端口 | 443 |

## 生产环境配置

### 1. 配置 HTTPS（推荐）

```bash
# 使用 Let's Encrypt 获取证书
sudo apt install certbot

# 停止 Nginx 容器
docker-compose stop nginx

# 获取证书
sudo certbot certonly --standalone -d your-domain.com

# 复制证书到项目目录
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/

# 重启 Nginx
docker-compose restart nginx
```

### 2. 配置防火墙

```bash
# 开放必要端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### 3. 数据库备份

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"

mkdir -p $BACKUP_DIR

docker-compose exec -T mysql mysqldump -u zulin -pZulin@2026! zulin > $BACKUP_DIR/zulin_$DATE.sql

echo "备份完成：$BACKUP_DIR/zulin_$DATE.sql"
```

## 故障排查

### 后端无法启动

```bash
# 查看日志
docker-compose logs backend

# 检查数据库连接
docker-compose exec backend python -c "from app.database import SessionLocal; db = SessionLocal(); print('OK')"
```

### 前端无法访问后端

1. 检查 `.env` 中的 `VITE_API_BASE_URL` 配置
2. 重新构建前端：`docker-compose build frontend`
3. 重启前端：`docker-compose restart frontend`

### 数据库连接失败

```bash
# 检查 MySQL 是否启动
docker-compose ps mysql

# 查看 MySQL 日志
docker-compose logs mysql

# 测试连接
docker-compose exec mysql mysql -u zulin -p -e "SHOW DATABASES;"
```

## 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build

# 执行数据库迁移（如果有）
docker-compose exec backend python migrate_add_user_id.py
```
