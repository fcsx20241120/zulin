#!/bin/bash
set -e

echo "========================================="
echo "  服务器离线部署脚本"
echo "========================================="

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查是否在服务器上运行
if [ ! -f "/etc/os-release" ]; then
    echo -e "${RED}错误：请在 Ubuntu 服务器上运行此脚本${NC}"
    exit 1
fi

echo -e "${YELLOW}步骤 1/6: 检查 Docker...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误：Docker 未安装${NC}"
    echo "请先安装 Docker:"
    echo "  curl -fsSL https://get.docker.com | sh"
    exit 1
fi

echo -e "${GREEN}✓ Docker 已安装：$(docker --version)${NC}"

echo -e "${YELLOW}步骤 2/6: 导入 Docker 镜像...${NC}"

cd /tmp

if [ ! -f "docker-images.tar.gz" ]; then
    echo -e "${RED}错误：未找到 docker-images.tar.gz${NC}"
    echo "请先上传镜像文件到 /tmp/"
    echo "  scp docker-images.tar.gz root@$(hostname -I | cut -d' ' -f1):/tmp/"
    exit 1
fi

tar -xzf docker-images.tar.gz

docker load < nginx-alpine.tar
echo "  - nginx:alpine ✓"

docker load < python-3.11-slim.tar
echo "  - python:3.11-slim ✓"

docker load < node-20-alpine.tar
echo "  - node:20-alpine ✓"

echo -e "${GREEN}✓ 镜像导入完成${NC}"

echo -e "${YELLOW}步骤 3/6: 配置项目...${NC}"

PROJECT_DIR="/data/www/zulin"

if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}项目目录不存在，正在克隆...${NC}"
    mkdir -p /data/www
    git clone https://github.com/fcsx20241120/zulin.git "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}已创建 .env 文件，请编辑配置 MySQL 等信息${NC}"
fi

echo -e "${GREEN}✓ 项目配置完成${NC}"

echo -e "${YELLOW}步骤 4/6: 创建必要目录...${NC}"

mkdir -p out nginx/ssl
[ -f "ht.docx" ] && cp ht.docx out/

echo -e "${GREEN}✓ 目录创建完成${NC}"

echo -e "${YELLOW}步骤 5/6: 构建并启动服务...${NC}"

docker compose down 2>/dev/null || true
docker compose build
docker compose up -d

echo -e "${GREEN}✓ 服务启动完成${NC}"

echo -e "${YELLOW}步骤 6/6: 初始化数据库...${NC}"

sleep 5
docker compose exec -T backend python init_db.py

echo -e "${GREEN}✓ 数据库初始化完成${NC}"

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "服务状态："
docker compose ps
echo ""
echo "访问地址："
echo -e "  前端：${GREEN}http://$(curl -s ifconfig.me 2>/dev/null || echo 'server-ip'):8088${NC}"
echo -e "  后端：${GREEN}http://$(curl -s ifconfig.me 2>/dev/null || echo 'server-ip'):8088/api/${NC}"
echo ""
echo "常用命令："
echo "  docker compose logs -f      # 查看日志"
echo "  docker compose ps           # 查看状态"
echo "  docker compose restart      # 重启服务"
echo ""
