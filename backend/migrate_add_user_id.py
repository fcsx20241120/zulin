"""
数据库迁移脚本：为所有表添加 user_id 字段
"""

from sqlalchemy import create_engine, text, inspect
import os

# 数据库连接字符串 - 使用 MySQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/zulin?charset=utf8mb4"
)


def migrate():
    """执行数据库迁移"""
    print(f"连接到数据库：{DATABASE_URL}")
    engine = create_engine(DATABASE_URL)

    # 获取所有表名
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"数据库中的表：{tables}")

    # 需要添加 user_id 字段的表
    target_tables = ["tenants", "landlords", "houses", "leases"]

    with engine.connect() as conn:
        for table in target_tables:
            if table not in tables:
                print(f"表 {table} 不存在，跳过")
                continue

            # 检查是否已有 user_id 字段
            columns = [col["name"] for col in inspector.get_columns(table)]
            if "user_id" in columns:
                print(f"表 {table} 已存在 user_id 字段，跳过")
                continue

            print(f"为表 {table} 添加 user_id 字段...")

            # MySQL 添加字段
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN user_id INT AFTER id"))

            # 创建索引
            conn.execute(text(f"CREATE INDEX idx_{table}_user_id ON {table}(user_id)"))

            print(f"✓ 表 {table} 迁移完成")

        conn.commit()

    print("\n迁移完成！")
    print("\n注意：现有数据的 user_id 字段为空，需要手动更新或重新创建数据")


if __name__ == "__main__":
    migrate()
