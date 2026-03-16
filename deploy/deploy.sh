#!/bin/bash

# 房屋租赁合同管理系统 - Ubuntu 部署脚本
# 使用方式：sudo bash deploy.sh

set -e

# 配置变量
APP_NAME="zulin"
APP_DIR="/var/www/zulin"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="/var/log/zulin"
FRONTEND_DIST="$APP_DIR/frontend/dist"
NGINX_SITES_AVAILABLE="/etc/nginx/sites-available"
NGINX_SITES_ENABLED="/etc/nginx/sites-enabled"

echo "=========================================="
echo "开始部署 $APP_NAME"
echo "=========================================="

# 1. 创建目录和日志文件
echo "[1/10] 创建目录结构..."
mkdir -p $APP_DIR
mkdir -p $LOG_DIR
touch $LOG_DIR/gunicorn_access.log
touch $LOG_DIR/gunicorn_error.log
touch $LOG_DIR/backend_err.log
touch $LOG_DIR/backend_out.log
chown -R www-data:www-data $LOG_DIR

# 2. 上传项目文件（需要手动执行）
echo "[2/10] 请上传项目文件到 $APP_DIR"
echo "      后端代码 -> $APP_DIR/backend"
echo "      前端代码 -> $APP_DIR/frontend"
echo "      依赖文件 -> $APP_DIR/requirements.txt, $APP_DIR/frontend/package.json"
read -p "按回车继续..."

# 3. 安装系统依赖
echo "[3/10] 安装系统依赖..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx

# 安装 Node.js 20+（Vite 要求）
if ! command -v node &> /dev/null || [[ $(node -v | cut -d'v' -f2 | cut -d'.' -f1) -lt 20 ]]; then
    echo "安装 Node.js 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# 4. 创建虚拟环境并安装 Python 依赖
echo "[4/10] 配置 Python 虚拟环境..."
cd $APP_DIR
python3 -m venv venv
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install gunicorn uvicorn
cd $APP_DIR/backend
pip install -r requirements.txt

# 5. 安装前端依赖并构建
echo "[5/10] 构建前端..."
cd $APP_DIR/frontend
npm install
npx vite build

# 6. 复制前端静态文件到 Nginx 目录
echo "[6/10] 部署前端静态文件..."
mkdir -p /var/www/zulin/frontend
cp -r $FRONTEND_DIST/* /var/www/zulin/frontend/
chown -R www-data:www-data /var/www/zulin/frontend

# 7. 配置环境变量
echo "[7/10] 配置环境变量..."
cp $APP_DIR/deploy/.env.production $APP_DIR/backend/.env
# 提示用户编辑环境变量
echo "请编辑 $APP_DIR/backend/.env 文件，配置数据库和密码"
read -p "编辑完成后按回车继续..."

# 8. 配置 Nginx
echo "[8/10] 配置 Nginx..."
cp $APP_DIR/deploy/nginx.conf $NGINX_SITES_AVAILABLE/$APP_NAME
ln -sf $NGINX_SITES_AVAILABLE/$APP_NAME $NGINX_SITES_ENABLED/$APP_NAME
rm -f $NGINX_SITES_ENABLED/default
nginx -t
systemctl reload nginx

# 9. 配置 Supervisor
echo "[9/10] 配置 Supervisor..."
cp $APP_DIR/deploy/supervisor.conf /etc/supervisor/conf.d/$APP_NAME.conf
cp $APP_DIR/deploy/gunicorn.conf.py $APP_DIR/backend/
supervisorctl reread
supervisorctl update
supervisorctl start $APP_NAME\_backend

# 10. 配置数据库
echo "[10/10] 配置数据库..."
echo ""
echo "=========================================="
echo "请配置数据库账号密码"
echo "=========================================="
echo ""
echo "选项 1：使用脚本自动创建（推荐）"
echo "选项 2：手动配置已有数据库"
echo ""
read -p "是否自动创建数据库？(y/n): " CREATE_DB

if [ "$CREATE_DB" = "y" ]; then
    # 设置数据库密码
    read -p "设置数据库密码：" -s DB_PASSWORD
    echo ""
    
    mysql -e "CREATE DATABASE IF NOT EXISTS zulin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    mysql -e "CREATE USER IF NOT EXISTS 'zulin_user'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
    mysql -e "GRANT ALL PRIVILEGES ON zulin.* TO 'zulin_user'@'localhost';"
    mysql -e "FLUSH PRIVILEGES;"
    
    # 更新 .env 文件
    sed -i "s/MYSQL_PASSWORD=.*/MYSQL_PASSWORD=$DB_PASSWORD/" $APP_DIR/backend/.env
    echo "✓ 数据库创建成功"
else
    echo "请手动编辑 $APP_DIR/backend/.env 文件，配置数据库信息："
    echo ""
    echo "  MYSQL_HOST=localhost"
    echo "  MYSQL_PORT=3306"
    echo "  MYSQL_DATABASE=zulin"
    echo "  MYSQL_USER=你的数据库用户名"
    echo "  MYSQL_PASSWORD=你的数据库密码"
    echo ""
    sudo nano $APP_DIR/backend/.env
fi

# 初始化数据库表
echo "初始化数据库表..."
cd $APP_DIR/backend
source $VENV_DIR/bin/activate
python -c "
from app.database import engine, Base
from app.models import *
Base.metadata.create_all(bind=engine)
print('数据库表创建成功')
"

echo ""
echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo "访问地址：http://your_server_ip"
echo ""
echo "重要：请记录数据库配置信息"
echo "配置文件：$APP_DIR/backend/.env"
echo ""
echo "管理命令："
echo "  查看后端日志：tail -f $LOG_DIR/backend_out.log"
echo "  查看 Supervisor 状态：supervisorctl status"
echo "  重启后端服务：supervisorctl restart zulin_backend"
echo "=========================================="
