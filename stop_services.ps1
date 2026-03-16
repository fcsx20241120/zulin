# 停止所有服务脚本

Write-Host "正在停止服务..." -ForegroundColor Yellow

# 停止所有 Python 进程
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 停止所有 Node 进程
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "所有服务已停止！" -ForegroundColor Green
