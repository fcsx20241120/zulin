"""
租赁合同模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Lease(Base):
    """租赁合同表"""

    __tablename__ = "leases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )  # 所属用户 ID

    # 关联信息
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    landlord_id = Column(Integer, ForeignKey("landlords.id"))
    house_id = Column(Integer, ForeignKey("houses.id"))

    # 租赁信息
    lease_years = Column(Integer)  # 租赁期限（年）
    start_date = Column(DateTime)  # 起租日期
    end_date = Column(DateTime)  # 终止日期
    monthly_rent = Column(Float)  # 月租金
    payment_type = Column(String(20))  # 支付方式（月付/季付/年付）
    deposit = Column(Float)  # 保证金

    # 费用承担
    water_fee = Column(String(20))  # 水费承担方
    electricity_fee = Column(String(20))  # 电费承担方
    gas_fee = Column(String(20))  # 燃气费承担方
    property_fee = Column(String(20))  # 物业费承担方

    # 家具电器清单（JSON 格式存储）
    furniture_list = Column(Text)  # 家具电器清单

    # 合同状态
    status = Column(
        String(20), default="active"
    )  # active: 有效，expired: 到期，terminated: 终止

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系定义
    tenant = relationship("Tenant", back_populates="leases")
    landlord = relationship("Landlord", back_populates="leases")
    house = relationship("House", back_populates="leases")
    owner = relationship("User", back_populates="leases")
