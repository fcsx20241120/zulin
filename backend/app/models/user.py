"""
用户模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """用户表"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    role = Column(String(20), default="user")  # admin: 管理员，user: 普通用户
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系定义
    tenants = relationship("Tenant", back_populates="owner")
    landlords = relationship("Landlord", back_populates="owner")
    houses = relationship("House", back_populates="owner")
    leases = relationship("Lease", back_populates="owner")
