"""
数据库配置模块
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class DBConfig:
    """数据库配置类"""

    # MySQL 连接配置
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "zulin")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

    # 连接池配置
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 5))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 10))

    @classmethod
    def get_sqlalchemy_url(cls) -> str:
        """获取 SQLAlchemy 数据库 URL"""
        return (
            f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}"
            f"@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}"
            f"?charset=utf8mb4"
        )

    @classmethod
    def get_connection_config(cls) -> dict:
        """获取数据库连接配置字典"""
        return {
            "host": cls.MYSQL_HOST,
            "port": cls.MYSQL_PORT,
            "database": cls.MYSQL_DATABASE,
            "user": cls.MYSQL_USER,
            "password": cls.MYSQL_PASSWORD,
            "charset": "utf8mb4",
        }
