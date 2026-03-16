"""
公告模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from app.database import Base


class Announcement(Base):
    """公告表"""

    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # 标题
    content = Column(Text, nullable=False)  # 内容
    type = Column(String(20), default="user")  # user: 用户公告，system: 系统公告
    is_published = Column(Boolean, default=True)  # 是否发布
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
