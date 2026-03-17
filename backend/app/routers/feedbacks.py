"""
用户反馈管理路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from jose import JWTError

from app.database import get_db
from app.models.feedback import Feedback
from app.models.user import User
from app.routers.auth import oauth2_scheme, jwt, SECRET_KEY, ALGORITHM

router = APIRouter()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """获取当前登录用户"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效令牌")
    except JWTError:
        raise HTTPException(status_code=401, detail="令牌验证失败")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


def is_admin(user: User) -> bool:
    """判断是否为管理员"""
    return user.role == "admin"


class FeedbackCreate(BaseModel):
    content: str


class FeedbackReply(BaseModel):
    reply: str
    status: str = "replied"


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    content: str
    reply: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    username: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=FeedbackResponse)
def create_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建用户反馈"""
    db_feedback = Feedback(**feedback_data.model_dump(), user_id=current_user.id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.get("/my", response_model=List[FeedbackResponse])
def get_my_feedbacks(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取当前用户的反馈列表"""
    if limit > 100:
        limit = 100

    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.user_id == current_user.id)
        .order_by(Feedback.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # 添加用户名
    result = []
    for fb in feedbacks:
        fb_dict = {
            "id": fb.id,
            "user_id": fb.user_id,
            "content": fb.content,
            "reply": fb.reply,
            "status": fb.status,
            "created_at": fb.created_at,
            "updated_at": fb.updated_at,
            "username": current_user.username,
        }
        result.append(FeedbackResponse(**fb_dict))

    return result


@router.get("/", response_model=List[FeedbackResponse])
def get_all_feedbacks(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取所有反馈列表（仅管理员）"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="无权访问")

    if limit > 100:
        limit = 100

    query = db.query(Feedback).join(User).order_by(Feedback.created_at.desc())

    if status:
        query = query.filter(Feedback.status == status)

    feedbacks = query.offset(skip).limit(limit).all()

    # 添加用户名
    result = []
    for fb in feedbacks:
        fb_dict = {
            "id": fb.id,
            "user_id": fb.user_id,
            "content": fb.content,
            "reply": fb.reply,
            "status": fb.status,
            "created_at": fb.created_at,
            "updated_at": fb.updated_at,
            "username": fb.user.username if fb.user else None,
        }
        result.append(FeedbackResponse(**fb_dict))

    return result


@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取反馈详情"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")

    # 普通用户只能查看自己的反馈
    if not is_admin(current_user) and feedback.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看")

    fb_dict = {
        "id": feedback.id,
        "user_id": feedback.user_id,
        "content": feedback.content,
        "reply": feedback.reply,
        "status": feedback.status,
        "created_at": feedback.created_at,
        "updated_at": feedback.updated_at,
        "username": feedback.user.username if feedback.user else None,
    }
    return FeedbackResponse(**fb_dict)


@router.post("/{feedback_id}/reply", response_model=FeedbackResponse)
def reply_feedback(
    feedback_id: int,
    reply_data: FeedbackReply,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """回复反馈（仅管理员）"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="无权操作")

    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")

    feedback.reply = reply_data.reply
    feedback.status = reply_data.status
    feedback.updated_at = datetime.now()

    db.commit()
    db.refresh(feedback)

    fb_dict = {
        "id": feedback.id,
        "user_id": feedback.user_id,
        "content": feedback.content,
        "reply": feedback.reply,
        "status": feedback.status,
        "created_at": feedback.created_at,
        "updated_at": feedback.updated_at,
        "username": feedback.user.username if feedback.user else None,
    }
    return FeedbackResponse(**fb_dict)


@router.delete("/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除反馈（仅管理员）"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="无权操作")

    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")

    db.delete(feedback)
    db.commit()
    return {"message": "删除成功"}
