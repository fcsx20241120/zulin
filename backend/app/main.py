"""
FastAPI 应用主文件
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import (
    auth,
    users,
    landlords,
    tenants,
    houses,
    leases,
    announcements,
    feedbacks,
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 从环境变量读取 CORS 配置
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")

app = FastAPI(
    title="房屋租赁合同管理系统 API",
    description="基于 Python + Vue3 的房屋租赁合同管理平台",
    version="1.0.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(landlords.router, prefix="/api/landlords", tags=["房东管理"])
app.include_router(tenants.router, prefix="/api/tenants", tags=["租客管理"])
app.include_router(houses.router, prefix="/api/houses", tags=["房屋管理"])
app.include_router(leases.router, prefix="/api/leases", tags=["租赁管理"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["公告管理"])
app.include_router(feedbacks.router, prefix="/api/feedbacks", tags=["反馈管理"])


@app.get("/")
def read_root():
    return {"message": "欢迎使用房屋租赁合同管理系统 API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
