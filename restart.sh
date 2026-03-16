#!/bin/bash
set -e

echo "重启所有服务..."
docker-compose restart 2>/dev/null || docker compose restart

echo "完成！"
