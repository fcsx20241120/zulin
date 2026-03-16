# 快速部署脚本 - Ubuntu 24.04

set -e

echo "========================================="
echo "  房屋租赁合同管理系统 - 快速部署"
echo "========================================="

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}正在安装 Docker...${NC}"
    curl -fsSL https://get.docker.com | sh
fi

# 检查 Docker Compose
if ! docker compose version &> /dev/null; then
    echo -e "${YELLOW}正在安装 Docker Compose...${NC}"
    apt update && apt install -y docker-compose-plugin
fi

echo -e "${GREEN}✓ Docker 已就绪${NC}"

# 创建 .env 文件
cat > .env << EOF
# MySQL 数据库配置
MYSQL_HOST=59.110
MYSQL_PORT=3306
MYSQL_DATABASE=zulin
MYSQL_USER=root
MYSQL_PASSWORD=1q2w3e4r

# JWT 配置
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 前端 API 地址
VITE_API_BASE_URL=http://localhost:8000

# Nginx 端口
HTTP_PORT=8088
HTTPS_PORT=8089
EOF

echo -e "${GREEN}✓ 配置文件已生成${NC}"

# 创建目录
mkdir -p out nginx/ssl

# 复制模板文件
[ -f "ht.docx" ] && cp ht.docx out/ 2>/dev/null || true

# 停止旧服务
echo -e "${YELLOW}清理旧服务...${NC}"
docker compose down --remove-orphans 2>/dev/null || true

# 构建并启动
echo -e "${YELLOW}构建并启动服务（这可能需要几分钟）...${NC}"
docker compose up -d --build

# 等待启动
sleep 10

# 初始化数据库
echo -e "${YELLOW}初始化数据库表结构...${NC}"
docker compose exec -T backend python init_db.py

# 显示状态
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "访问地址："
echo -e "  前端：${GREEN}http://$(curl -s ifconfig.me 2>/dev/null || echo 'your-server-ip'):8088${NC}"
echo -e "  后端：${GREEN}http://$(curl -s ifconfig.me 2>/dev/null || echo 'your-server-ip'):8088/api/${NC}"
echo ""
echo "常用命令："
echo "  docker compose logs -f        # 查看日志"
echo "  docker compose ps             # 查看状态"
echo "  docker compose restart        # 重启服务"
echo ""
