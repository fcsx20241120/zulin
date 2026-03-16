# 服务管理脚本 - 在新窗口启动前后端服务

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# 启动后端服务
Start-Process powershell -ArgumentList @"
-NoExit -Command "
    Write-Host '=== 启动后端服务 ===' -ForegroundColor Green
    cd '$projectRoot\backend'
    .\venv\Scripts\Activate.ps1
    python main.py
"
"@

# 等待 1 秒
Start-Sleep -Seconds 1

# 启动前端服务
Start-Process powershell -ArgumentList @"
-NoExit -Command "
    Write-Host '=== 启动前端服务 ===' -ForegroundColor Cyan
    cd '$projectRoot\frontend'
    npm run dev
"
"@

Write-Host "服务已在新窗口启动！" -ForegroundColor Green
Write-Host "后端：http://localhost:8000" -ForegroundColor Yellow
Write-Host "前端：http://localhost:5173" -ForegroundColor Yellow
