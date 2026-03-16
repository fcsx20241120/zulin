"""
创建默认管理员账号
"""

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.routers.auth import get_password_hash

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建管理员账号
db = SessionLocal()
try:
    # 检查是否已有管理员
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        print("管理员账号已存在")
    else:
        admin = User(
            username="admin",
            password=get_password_hash("admin123"),
            email="admin@example.com",
            role="admin",
        )
        db.add(admin)
        db.commit()
        print("=" * 50)
        print("管理员账号创建成功！")
        print("账号：admin")
        print("密码：admin123")
        print("=" * 50)
finally:
    db.close()
