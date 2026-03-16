#!/bin/bash

echo "查看服务日志..."
echo ""
echo "按 Ctrl+C 退出日志查看"
echo ""

docker-compose logs -f "$@" 2>/dev/null || docker compose logs -f "$@"
