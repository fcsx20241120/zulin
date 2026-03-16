# Docker Image Packaging Script for Windows
# Run as Administrator in PowerShell

Write-Host "=== Docker Image Packaging ==="

$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$images = "nginx:alpine", "python:3.11-slim", "node:20-alpine"

Write-Host "Pulling images..."
foreach ($img in $images) { docker pull $img }

Write-Host "Saving images..."
foreach ($img in $images) {
    $name = $img -replace ':', '-'
    docker save -o "$dir\$name.tar" $img
}

Write-Host "Compressing..."
Compress-Archive -Path "$dir\*.tar" -DestinationPath "$dir\docker-images.tar.gz" -Force

Write-Host "Cleaning..."
Remove-Item "$dir\*.tar" -Force

Write-Host "Done: $dir\docker-images.tar.gz"
Write-Host "Upload to server: scp docker-images.tar.gz root@59.110.139.122:/tmp/"
