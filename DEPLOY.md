# 使用现有 MySQL 部署指南

## 前置要求

- Ubuntu 24.04 LTS
- Docker 20.10+
- Docker Compose 2.0+
- **现有 MySQL 8.0+ 服务器**

## 部署步骤

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

# 添加当前用户到 docker 组
sudo usermod -aG docker $USER
newgrp docker
```

### 2. 配置 MySQL 数据库

```bash
# 登录 MySQL
mysql -u root -p

# 执行初始化脚本（或手动执行）
source mysql/init_external.sql
```

**或者手动执行 SQL：**

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS zulin DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER IF NOT EXISTS 'zulin'@'%' IDENTIFIED BY 'Zulin@2026!';

-- 授权
GRANT ALL PRIVILEGES ON zulin.* TO 'zulin'@'%';
FLUSH PRIVILEGES;
```

### 3. 配置应用

```bash
# 克隆项目
git clone https://github.com/fcsx20241120/zulin.git
cd zulin

# 复制配置文件
cp .env.example .env

# 编辑配置
vim .env
```

**修改 .env 文件：**

```bash
# MySQL 配置（使用现有数据库）
MYSQL_HOST=127.0.0.1          # 如果在同一台服务器，使用 127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=zulin
MYSQL_USER=zulin
MYSQL_PASSWORD=Zulin@2026!    # 修改为你的密码

# JWT 配置（修改为随机字符串）
SECRET_KEY=your-random-secret-key-at-least-32-characters-long

# 前端 API 地址
VITE_API_BASE_URL=http://localhost:8000

# Nginx 端口
HTTP_PORT=80
```

### 4. 部署应用

```bash
# 执行部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 5. 初始化数据库表结构

```bash
# 进入后端容器
docker-compose exec backend bash

# 初始化数据库
python init_db.py

# 退出容器
exit
```

### 6. 访问应用

- 前端：http://your-server-ip
- 后端 API: http://your-server-ip/api/

---

## MySQL 连接配置说明

### 场景 1：MySQL 在同一台服务器

```bash
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

### 场景 2：MySQL 在局域网其他服务器

```bash
MYSQL_HOST=192.168.1.50     # MySQL 服务器内网 IP
MYSQL_PORT=3306
```

确保：
1. MySQL 允许远程连接：`CREATE USER 'zulin'@'%' ...`
2. 防火墙开放 3306 端口
3. MySQL 配置 `bind-address = 0.0.0.0`

### 场景 3：MySQL 在云服务器（如 RDS）

```bash
MYSQL_HOST=rm-xxxxx.mysql.rds.aliyuncs.com   # RDS 连接地址
MYSQL_PORT=3306
MYSQL_DATABASE=zulin
MYSQL_USER=zulin
MYSQL_PASSWORD=your-password
```

确保：
1. RDS 白名单包含 Docker 服务器 IP
2. 安全组开放 3306 端口

---

## 故障排查

### 后端无法连接 MySQL

```bash
# 查看后端日志
docker-compose logs backend

# 测试数据库连接
docker-compose exec backend python -c "
from app.database import SessionLocal
try:
    db = SessionLocal()
    db.execute('SELECT 1')
    print('数据库连接成功')
except Exception as e:
    print(f'数据库连接失败：{e}')
"
```

### 常见错误

**错误 1：Access denied for user**
```
解决：检查 .env 中的 MYSQL_USER 和 MYSQL_PASSWORD 是否正确
```

**错误 2：Can't connect to MySQL server**
```
解决：
1. 检查 MYSQL_HOST 和 MYSQL_PORT 是否正确
2. 确保 MySQL 服务正在运行
3. 检查防火墙设置
```

**错误 3：Unknown database 'zulin'**
```
解决：执行 MySQL 初始化脚本创建数据库
```

---

## 常用运维命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f nginx

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 重新构建并启动
docker-compose up -d --build

# 进入容器
docker-compose exec backend bash

# 查看数据库连接
docker-compose exec backend python -c "from app.database import SessionLocal; print(SessionLocal().execute('SELECT 1').fetchone())"
```

---

## 数据备份

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
MYSQL_HOST="127.0.0.1"
MYSQL_USER="root"
MYSQL_PASSWORD="your-root-password"
MYSQL_DATABASE="zulin"

mkdir -p $BACKUP_DIR

mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > $BACKUP_DIR/zulin_$DATE.sql

echo "备份完成：$BACKUP_DIR/zulin_$DATE.sql"
```

---

## 安全建议

1. **修改默认密码**：修改 `.env` 中的所有默认密码
2. **SECRET_KEY**：使用随机生成的 32+ 字符密钥
3. **MySQL 用户权限**：只授予必要的权限
4. **防火墙**：只开放必要的端口（80/443）
5. **定期备份**：设置定时任务备份数据库
6. **HTTPS**：生产环境使用 HTTPS（配置 SSL 证书）
