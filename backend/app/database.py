"""
数据库连接模块
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DBConfig

# 从环境变量读取调试模式，默认为开发环境
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# 创建数据库引擎
engine = create_engine(
    DBConfig.get_sqlalchemy_url(),
    pool_size=DBConfig.DB_POOL_SIZE,
    max_overflow=DBConfig.DB_MAX_OVERFLOW,
    echo=DEBUG,  # 开发环境开启 SQL 日志
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
