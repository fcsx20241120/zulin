#!/bin/bash
set -e

echo "========================================="
echo "  Docker 镜像打包脚本"
echo "========================================="

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 创建输出目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/images"
mkdir -p "$OUTPUT_DIR"

echo -e "${YELLOW}步骤 1/4: 拉取基础镜像...${NC}"

# 拉取镜像（如果本地没有）
docker pull docker.io/library/nginx:alpine || true
docker pull docker.io/library/python:3.11-slim || true
docker pull docker.io/library/node:20-alpine || true

echo -e "${GREEN}✓ 镜像拉取完成${NC}"

echo -e "${YELLOW}步骤 2/4: 保存镜像为 tar 文件...${NC}"

# 保存镜像
docker save docker.io/library/nginx:alpine -o "$OUTPUT_DIR/nginx-alpine.tar"
echo "  - nginx:alpine ✓"

docker save docker.io/library/python:3.11-slim -o "$OUTPUT_DIR/python-3.11-slim.tar"
echo "  - python:3.11-slim ✓"

docker save docker.io/library/node:20-alpine -o "$OUTPUT_DIR/node-20-alpine.tar"
echo "  - node:20-alpine ✓"

echo -e "${GREEN}✓ 镜像保存完成${NC}"

echo -e "${YELLOW}步骤 3/4: 压缩镜像文件...${NC}"

# 压缩
cd "$OUTPUT_DIR"
tar -czf ../docker-images.tar.gz *.tar

# 获取文件大小
FILE_SIZE=$(du -h ../docker-images.tar.gz | cut -f1)

echo -e "${GREEN}✓ 压缩完成：../docker-images.tar.gz (${FILE_SIZE})${NC}"

echo -e "${YELLOW}步骤 4/4: 清理临时文件...${NC}"

# 清理 tar 文件
rm -f *.tar

echo -e "${GREEN}✓ 清理完成${NC}"

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  打包完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "文件位置：$SCRIPT_DIR/docker-images.tar.gz"
echo "文件大小：$FILE_SIZE"
echo ""
echo "上传到服务器的命令："
echo "  scp $SCRIPT_DIR/docker-images.tar.gz root@59.110.139.122:/tmp/"
echo ""
echo "在服务器上导入的命令："
echo "  cd /tmp"
echo "  tar -xzf docker-images.tar.gz"
echo "  docker load < nginx-alpine.tar"
echo "  docker load < python-3.11-slim.tar"
echo "  docker load < node-20-alpine.tar"
echo ""
