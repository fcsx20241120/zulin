# Docker 镜像打包脚本 - Windows PowerShell
# 在 Windows 11 上以管理员身份运行 PowerShell 执行此脚本

$ErrorActionPreference = "Stop"

Write-Host "========================================="
Write-Host "  Docker 镜像打包脚本 (Windows)"
Write-Host "========================================="
Write-Host ""

# 获取脚本所在目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $ScriptDir "images"

# 创建输出目录
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    Write-Host "[OK] 创建输出目录：$OutputDir"
}

Write-Host ""
Write-Host "步骤 1/4: 拉取基础镜像..."

# 拉取镜像
$images = @(
    "docker.io/library/nginx:alpine",
    "docker.io/library/python:3.11-slim",
    "docker.io/library/node:20-alpine"
)

foreach ($image in $images) {
    Write-Host "  拉取：$image" -NoNewline
    $result = docker pull $image 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK]"
    } else {
        Write-Host " [已存在]"
    }
}

Write-Host ""
Write-Host "步骤 2/4: 保存镜像为 tar 文件..."

# 保存镜像
$tarFiles = @()
foreach ($image in $images) {
    $imageName = ($image -replace 'docker.io/library/', '') -replace ':', '-'
    $tarFile = Join-Path $OutputDir "$imageName.tar"
    $tarFiles += $tarFile
    
    Write-Host "  保存：$image" -NoNewline
    docker save -o $tarFile $image
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK]"
    } else {
        Write-Host " [失败]"
        exit 1
    }
}

Write-Host ""
Write-Host "步骤 3/4: 压缩镜像文件..."

# 压缩文件
$compressedFile = Join-Path $ScriptDir "docker-images.tar.gz"

# 使用 PowerShell 压缩
Compress-Archive -Path $tarFiles -DestinationPath $compressedFile -CompressionLevel Optimal -Force

if (Test-Path $compressedFile) {
    $fileSize = Get-ChildItem $compressedFile | ForEach-Object { 
        $size = $_.Length
        if ($size -gt 1GB) { "{0:F2} GB" -f ($size / 1GB) }
        elseif ($size -gt 1MB) { "{0:F2} MB" -f ($size / 1MB) }
        else { "{0:F2} KB" -f ($size / 1KB) }
    }
    Write-Host "  压缩完成：$compressedFile ($fileSize)"
} else {
    Write-Host "  压缩失败！"
    exit 1
}

Write-Host ""
Write-Host "步骤 4/4: 清理临时文件..."

# 清理 tar 文件
foreach ($tarFile in $tarFiles) {
    Remove-Item -Path $tarFile -Force
}

Write-Host "  清理完成"

Write-Host ""
Write-Host "========================================="
Write-Host "  打包完成！"
Write-Host "========================================="
Write-Host ""
Write-Host "文件位置：$compressedFile"
Write-Host ""
Write-Host "上传到服务器的方法:"
Write-Host ""
Write-Host "  1. 使用 WinSCP (推荐):"
Write-Host "     下载：https://winscp.net/"
Write-Host "     主机：59.110.139.122, 用户：root"
Write-Host ""
Write-Host "  2. 使用 PowerShell:"
Write-Host "     scp `"$compressedFile`" root@59.110.139.122:/tmp/"
Write-Host ""
Write-Host "  3. 使用 Git Bash:"
Write-Host "     scp `"$compressedFile`" root@59.110.139.122:/tmp/"
Write-Host ""
Write-Host "在服务器上导入:"
Write-Host ""
Write-Host "  ssh root@59.110.139.122"
Write-Host "  cd /tmp"
Write-Host "  tar -xzf docker-images.tar.gz"
Write-Host "  docker load < nginx-alpine.tar"
Write-Host "  docker load < python-3.11-slim.tar"
Write-Host "  docker load < node-20-alpine.tar"
Write-Host ""
