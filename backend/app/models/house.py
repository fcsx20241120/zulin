"""
房屋模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class House(Base):
    """房屋表"""

    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )  # 所属用户 ID
    address = Column(String(255), nullable=False)  # 房屋地址
    area = Column(Float)  # 面积（平方米）
    usage = Column(String(50))  # 房屋用途
    property_cert = Column(String(100))  # 产权证号
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系定义
    leases = relationship("Lease", back_populates="house")
    owner = relationship("User", back_populates="houses")
