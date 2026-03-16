# 房屋租赁合同管理系统

基于 Python + Vue3 的房屋租赁合同管理平台，实现合同、租客、房屋、房东的信息化管理。

## 目录

- [技术栈](#技术栈)
- [功能模块](#功能模块)
- [数据结构](#数据结构)
- [快速开始](#快速开始)
- [API 接口](#api 接口)
- [开发指南](#开发指南)

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Element Plus + Pinia + Vue Router |
| 后端 | Python + FastAPI + SQLAlchemy |
| 数据库 | MySQL |
| 认证 | JWT |

## 功能模块

### 前台（用户端）

| 模块 | 功能描述 |
|------|----------|
| **首页** | 欢迎信息、用户公告、租赁提醒（7 天内到期合同列表） |
| **租赁** | 合同列表（时间倒序）、新增合同、合同详情 |
| **我的** | 注册/登录、用户信息、注销 |

### 管理后台

| 模块 | 功能描述 |
|------|----------|
| **首页** | 欢迎信息、系统公告、统计数据 |
| **合同管理** | 合同列表、增删改查 |
| **租客管理** | 租客列表、增删改查 |
| **房屋管理** | 房屋列表、增删改查 |
| **房东管理** | 房东列表、增删改查 |
| **系统管理** | 公告管理（用户/系统公告）、用户管理 |

## 数据结构

### 数据库表

- `users` - 用户表
- `landlords` - 房东表
- `tenants` - 租客表
- `houses` - 房屋表
- `leases` - 租赁合同表
- `announcements` - 公告表

详细字段请参考 `ht.md` 文件和 `backend/app/models/` 目录。

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置数据库（编辑 .env 文件）
cp ../.env.example .env
# 修改 .env 中的数据库配置

# 启动服务
python main.py
```

后端服务将在 http://localhost:8000 启动

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

## API 接口

### 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| GET | /api/auth/me | 获取当前用户 |

### 业务接口

| 模块 | 路径 | 描述 |
|------|------|------|
| 租赁 | /api/leases | 租赁合同 CRUD |
| 租客 | /api/tenants | 租客信息 CRUD |
| 房屋 | /api/houses | 房屋信息 CRUD |
| 房东 | /api/landlords | 房东信息 CRUD |
| 公告 | /api/announcements | 公告 CRUD |
| 用户 | /api/users | 用户管理（管理员） |

## 项目结构

```
zulin/
├── backend/              # 后端项目
│   ├── app/
│   │   ├── models/       # 数据模型
│   │   ├── routers/      # API 路由
│   │   ├── services/     # 业务逻辑
│   │   ├── database.py   # 数据库连接
│   │   └── main.py       # FastAPI 应用
│   ├── config.py         # 配置模块
│   ├── main.py           # 启动脚本
│   └── requirements.txt  # Python 依赖
├── frontend/             # 前端项目
│   ├── src/
│   │   ├── api/          # API 请求
│   │   ├── views/        # 页面组件
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── router/       # 路由配置
│   │   └── main.ts       # 入口文件
│   ├── index.html
│   └── package.json
├── .env                  # 环境变量配置
├── .env.example          # 环境变量模板
├── .gitignore
├── README.md
├── AGENTS.md
└── ht.md                 # 合同数据结构说明
```

## 开发指南

### 代码规范

- 前端：ESLint + TypeScript
- 后端：Black + Flake8 + MyPy
- 详见 `AGENTS.md`

### 默认管理员账号

首次启动需要手动创建管理员账号：

```python
# 在 backend 目录下执行
python -c "
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.routers.auth import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()
admin = User(username='admin', password=get_password_hash('admin123'), role='admin')
db.add(admin)
db.commit()
db.close()
print('管理员账号创建成功：admin/admin123')
"
```

## 待办事项

- [ ] 合同模板导入功能（docx 解析）
- [ ] 家具电器清单详细管理
- [ ] 数据导出功能
- [ ] 统计报表

## 许可证

MIT
