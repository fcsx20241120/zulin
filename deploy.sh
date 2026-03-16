#!/bin/bash
set -e

echo "========================================="
echo "  房屋租赁合同管理系统 - Docker 部署脚本"
echo "========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在项目根目录
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}错误：请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 检查 Docker 和 Docker Compose
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误：Docker 未安装${NC}"
    echo "请先安装 Docker: https://docs.docker.com/engine/install/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}错误：Docker Compose 未安装${NC}"
    echo "请先安装 Docker Compose"
    exit 1
fi

echo -e "${GREEN}✓ Docker 和 Docker Compose 已安装${NC}"

# 复制环境变量文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}创建 .env 配置文件...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}请修改 .env 文件中的 MySQL 连接配置${NC}"
fi

# 创建必要的目录
echo -e "${YELLOW}创建必要的目录...${NC}"
mkdir -p nginx/ssl
mkdir -p out

# 复制模板文件
if [ -f "ht.docx" ]; then
    cp ht.docx ./out/ 2>/dev/null || true
fi

# 停止并清理旧容器
echo -e "${YELLOW}停止并清理旧容器...${NC}"
docker-compose down --remove-orphans 2>/dev/null || docker compose down --remove-orphans

# 构建镜像
echo -e "${YELLOW}构建 Docker 镜像（这可能需要几分钟）...${NC}"
docker-compose build 2>/dev/null || docker compose build

# 启动服务
echo -e "${YELLOW}启动服务...${NC}"
docker-compose up -d 2>/dev/null || docker compose up -d

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo -e "${YELLOW}检查服务状态...${NC}"
docker-compose ps 2>/dev/null || docker compose ps

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "服务访问地址："
echo -e "  - 前端：${GREEN}http://localhost${NC}"
echo -e "  - 后端 API: ${GREEN}http://localhost/api/${NC}"
echo ""
echo "常用命令："
echo "  查看日志：docker-compose logs -f"
echo "  重启服务：docker-compose restart"
echo "  停止服务：docker-compose down"
echo "  查看状态：docker-compose ps"
echo ""

# 数据库检查
echo -e "${YELLOW}提示：请确保 MySQL 数据库已创建并配置正确${NC}"
echo "可以在 .env 文件中修改 MySQL 连接配置："
echo "  MYSQL_HOST=127.0.0.1"
echo "  MYSQL_PORT=3306"
echo "  MYSQL_DATABASE=zulin"
echo "  MYSQL_USER=zulin"
echo "  MYSQL_PASSWORD=your_password"
echo ""
