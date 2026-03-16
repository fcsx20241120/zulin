#!/bin/bash
set -e

echo "停止并清理所有容器..."
docker-compose down --remove-orphans 2>/dev/null || docker compose down --remove-orphans

echo "清理未使用的镜像和缓存..."
docker image prune -af
docker volume prune -f

echo "完成！"
