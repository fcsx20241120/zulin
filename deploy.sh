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
    echo -e "${GREEN}✓ 已创建 .env 文件，请根据实际情况修改配置${NC}"
fi

# 创建必要的目录
echo -e "${YELLOW}创建必要的目录...${NC}"
mkdir -p nginx/ssl
mkdir -p out
mkdir -p mysql

# 复制模板文件到 out 目录
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
sleep 15

# 检查服务状态
echo -e "${YELLOW}检查服务状态...${NC}"
docker-compose ps 2>/dev/null || docker compose ps

# 显示日志
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "服务访问地址："
echo "  - 前端：http://localhost"
echo "  - 后端 API: http://localhost/api/"
echo "  - MySQL: localhost:3306"
echo ""
echo "常用命令："
echo "  查看日志：docker-compose logs -f"
echo "  重启服务：docker-compose restart"
echo "  停止服务：docker-compose down"
echo "  查看状态：docker-compose ps"
echo ""

# 初始化数据库提示
echo -e "${YELLOW}提示：首次启动需要初始化数据库${NC}"
echo "请在后端容器中执行："
echo "  docker-compose exec backend python init_db.py"
echo ""
