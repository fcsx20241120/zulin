# Ubuntu 部署指南

## 部署方式：Nginx + Gunicorn + Supervisor

### 目录结构
```
/var/www/zulin/
├── backend/           # 后端代码
├── frontend/          # 前端代码（源码）
├── venv/              # Python 虚拟环境
└── deploy/            # 部署配置文件
```

## 快速部署

### 1. 准备服务器

```bash
# SSH 登录服务器
ssh user@your_server_ip

# 更新系统
sudo apt update && sudo apt upgrade -y
```

### 2. 上传项目文件

```bash
# 在本地执行（将项目上传到服务器）
scp -r backend/ deploy/ user@your_server_ip:/tmp/zulin/
scp -r frontend/ user@your_server_ip:/tmp/zulin/
```

### 3. 配置数据库账号密码 ⭐ 重要

```bash
# 登录 MySQL
sudo mysql -u root

# 在 MySQL 中执行（请修改密码为你的强密码）：
CREATE DATABASE IF NOT EXISTS zulin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'zulin_user'@'localhost' IDENTIFIED BY 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON zulin.* TO 'zulin_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**注意：** 请记住设置的密码，稍后需要填入 `.env` 文件中。

### 4. 执行部署脚本

```bash
# 在服务器上执行
sudo mv /tmp/zulin /var/www/zulin
cd /var/www/zulin
sudo bash deploy/deploy.sh
```

### 5. 修改配置

```bash
# 编辑环境变量（填入上面设置的数据库密码）
sudo nano /var/www/zulin/backend/.env
```

修改以下内容：
```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=zulin
MYSQL_USER=zulin_user
MYSQL_PASSWORD=YourSecurePassword123!  # 替换为你设置的密码
```

```bash
# 编辑 Nginx 配置（域名）
sudo nano /etc/nginx/sites-available/zulin
```

### 6. 重启服务

```bash
sudo supervisorctl restart zulin_backend
sudo systemctl reload nginx
```

## 手动部署步骤

### 安装依赖

```bash
# 系统依赖
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx supervisor

# ⭐ 安装 Node.js 20+（Vite 要求）
# 方法 1：使用 NodeSource（推荐）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 方法 2：如果方法 1 有依赖冲突，使用 nvm（最可靠）
# 卸载冲突的包
sudo apt remove --purge nodejs npm -y
sudo apt autoremove -y

# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# 使用 nvm 安装 Node.js 20
nvm install 20
nvm use 20
nvm alias default 20

# 方法 3：如果网络连接失败（无法访问 Docker/NodeSource 源）
# 使用国内镜像源（阿里云）
sudo tee /etc/apt/sources.list > /dev/null << 'EOF'
deb http://mirrors.aliyun.com/ubuntu noble main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu noble-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu noble-updates main restricted universe multiverse
EOF

sudo apt update
sudo apt install -y nodejs npm
```

**网络问题处理：**
如果遇到 `Could not handshake` 或 `Failed to fetch` 错误：
```bash
# 移除有问题的 Docker 源
sudo rm /etc/apt/sources.list.d/docker.list
sudo rm /etc/apt/keyrings/docker.gpg
sudo apt update
```

### 配置数据库账号密码 ⭐ 重要

```bash
# 登录 MySQL
sudo mysql

# 在 MySQL 中执行以下 SQL（请根据实际情况修改密码）：
-- 创建数据库
CREATE DATABASE IF NOT EXISTS zulin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（请将 'YourSecurePassword123!' 替换为你的强密码）
CREATE USER 'zulin_user'@'localhost' IDENTIFIED BY 'YourSecurePassword123!';

-- 授权
GRANT ALL PRIVILEGES ON zulin.* TO 'zulin_user'@'localhost';
FLUSH PRIVILEGES;

-- 退出 MySQL
EXIT;
```

**注意：** 
- 请将 `YourSecurePassword123!` 替换为你自己的强密码
- 记住设置的密码，稍后配置 `.env` 文件时需要使用
- 如果 MySQL 已存在 zulin 数据库，可跳过创建步骤，直接使用现有数据库

### 安装 Python 依赖

```bash
cd /var/www/zulin
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install gunicorn uvicorn
cd backend
pip install -r requirements.txt
```

### 构建前端

```bash
cd /var/www/zulin/frontend

# 安装依赖
npm install

# 构建项目（使用 npx 确保命令可执行）
npx vite build

# 复制静态文件到 Nginx 目录
cp -r dist/* /var/www/zulin/frontend/
```

如果遇到 `Permission denied` 错误，执行：
```bash
# 修复 node_modules 权限
chmod -R +x /var/www/zulin/frontend/node_modules/.bin/

# 或者重新安装依赖
rm -rf node_modules package-lock.json
npm install
```

### 配置环境变量 ⭐ 重要

```bash
# 复制生产环境配置
cp /var/www/zulin/deploy/.env.production /var/www/zulin/backend/.env

# 编辑配置文件
sudo nano /var/www/zulin/backend/.env
```

**必须修改以下内容：**
```bash
# MySQL 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=zulin
MYSQL_USER=zulin_user
MYSQL_PASSWORD=YourSecurePassword123!  # ⭐ 替换为你上面设置的密码

# JWT 配置（生产环境必须修改）
SECRET_KEY=your-random-secret-key-min-32-chars  # ⭐ 使用随机生成的密钥
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**生成随机 SECRET_KEY：**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 配置 Nginx

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/zulin
sudo ln -s /etc/nginx/sites-available/zulin /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 配置 Supervisor

```bash
sudo cp deploy/supervisor.conf /etc/supervisor/conf.d/zulin.conf
sudo cp deploy/gunicorn.conf.py /var/www/zulin/backend/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start zulin_backend
```

### 验证数据库连接

```bash
cd /var/www/zulin/backend
source /var/www/zulin/venv/bin/activate
python -c "
from app.database import engine
from sqlalchemy import text
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✓ 数据库连接成功')
except Exception as e:
    print(f'✗ 数据库连接失败：{e}')
"
```

### 构建前端

```bash
cd /var/www/zulin/frontend
npm install
npm run build
cp -r dist/* /var/www/zulin/frontend/
```

### 配置 Nginx

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/zulin
sudo ln -s /etc/nginx/sites-available/zulin /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 配置 Supervisor

```bash
sudo cp deploy/supervisor.conf /etc/supervisor/conf.d/zulin.conf
sudo cp deploy/gunicorn.conf.py /var/www/zulin/backend/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start zulin_backend
```

### 配置数据库

```bash
# 登录 MySQL
sudo mysql

# 创建数据库和用户
CREATE DATABASE IF NOT EXISTS zulin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'zulin_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON zulin.* TO 'zulin_user'@'localhost';
FLUSH PRIVILEGES;
exit;
```

## 常用命令

### 服务管理

```bash
# 查看服务状态
sudo supervisorctl status

# 重启后端
sudo supervisorctl restart zulin_backend

# 停止后端
sudo supervisorctl stop zulin_backend

# 查看后端日志
sudo tail -f /var/log/zulin/backend_out.log
sudo tail -f /var/log/zulin/backend_err.log

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 更新部署

```bash
cd /var/www/zulin

# 备份当前版本
sudo cp -r backend backend.bak
sudo cp -r frontend frontend.bak

# 上传新代码后...

# 重启后端
sudo supervisorctl restart zulin_backend

# 验证无误后删除备份
rm -rf backend.bak frontend.bak
```

## 安全建议

1. **修改默认密码**：确保 `.env` 文件中的密码足够复杂
2. **配置防火墙**：
   ```bash
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # HTTP
   sudo ufw allow 443/tcp   # HTTPS
   sudo ufw enable
   ```
3. **启用 HTTPS**（推荐）：
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your_domain.com
   ```
4. **定期备份数据库**：
   ```bash
   mysqldump -u zulin_user -p zulin > backup_$(date +%Y%m%d).sql
   ```

## 故障排查

### 后端无法启动

```bash
# 查看 Supervisor 日志
sudo tail -f /var/log/zulin/backend_err.log

# 检查 Python 依赖
source /var/www/zulin/venv/bin/activate
pip list

# 测试直接运行
cd /var/www/zulin/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Nginx 报错 502

```bash
# 检查后端是否运行
sudo supervisorctl status

# 检查 Nginx 配置
sudo nginx -t

# 查看 Nginx 错误日志
sudo tail -f /var/log/nginx/error.log
```

### 数据库连接失败

```bash
# 检查 MySQL 状态
sudo systemctl status mysql

# 测试数据库连接
mysql -u zulin_user -p -e "SHOW DATABASES;"

# 如果提示密码错误，重置密码：
sudo mysql
ALTER USER 'zulin_user'@'localhost' IDENTIFIED BY 'YourNewPassword123!';
FLUSH PRIVILEGES;
EXIT;

# 然后更新 .env 文件中的密码
sudo nano /var/www/zulin/backend/.env
```

## 性能优化建议

1. **调整 Gunicorn worker 数量**：
   ```python
   # gunicorn.conf.py
   workers = 4  # CPU 核心数 * 2 + 1
   ```

2. **启用 Nginx 缓存**：
   ```nginx
   proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m;
   ```

3. **配置 MySQL 优化**：
   ```bash
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   ```
