"""
用户反馈模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Feedback(Base):
    """用户反馈表"""

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )  # 用户 ID
    content = Column(Text, nullable=False)  # 反馈内容
    reply = Column(Text, nullable=True)  # 管理员回复
    status = Column(
        String(20), default="pending"
    )  # pending: 待处理，replied: 已回复，closed: 已关闭
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联用户
    user = relationship("User", backref="feedbacks")
