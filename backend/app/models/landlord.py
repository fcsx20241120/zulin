"""
房东模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Landlord(Base):
    """房东表"""

    __tablename__ = "landlords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )  # 所属用户 ID
    name = Column(String(100), nullable=False)  # 姓名/名称
    address = Column(String(255))  # 地址
    id_card = Column(String(50))  # 身份证号/统一社会信用代码
    phone = Column(String(20))  # 电话
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系定义
    leases = relationship("Lease", back_populates="landlord")
    owner = relationship("User", back_populates="landlords")
