# 服务管理配置

## 自动启动规则
- 代码修改后需要在新窗口自动启动/重启服务
- 用户不再手动操作启动命令

## 服务配置
- **后端服务**: 
  - 目录：`backend`
  - 命令：`venv\Scripts\activate && python main.py`
  - 端口：`8000`

- **前端服务**:
  - 目录：`frontend`
  - 命令：`npm run dev`
  - 端口：`5173`

## 启动脚本
使用 `start_services.ps1` 自动在新窗口启动服务
