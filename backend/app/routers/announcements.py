"""
公告管理路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models.announcement import Announcement

router = APIRouter()


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    type: str = "user"
    is_published: bool = True


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    is_published: Optional[bool] = None


class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    type: str
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=AnnouncementResponse)
def create_announcement(
    announcement_data: AnnouncementCreate, db: Session = Depends(get_db)
):
    """创建公告"""
    db_announcement = Announcement(**announcement_data.model_dump())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


@router.get("/", response_model=List[AnnouncementResponse])
def get_announcements(
    skip: int = 0,
    limit: int = 100,
    announcement_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """获取公告列表"""
    query = db.query(Announcement).filter(Announcement.is_published == True)

    if announcement_type:
        query = query.filter(Announcement.type == announcement_type)

    announcements = (
        query.order_by(Announcement.created_at.desc()).offset(skip).limit(limit).all()
    )
    return announcements


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
def get_announcement(announcement_id: int, db: Session = Depends(get_db)):
    """获取公告详情"""
    announcement = (
        db.query(Announcement).filter(Announcement.id == announcement_id).first()
    )
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")
    return announcement


@router.put("/{announcement_id}", response_model=AnnouncementResponse)
def update_announcement(
    announcement_id: int,
    announcement_data: AnnouncementUpdate,
    db: Session = Depends(get_db),
):
    """更新公告信息"""
    announcement = (
        db.query(Announcement).filter(Announcement.id == announcement_id).first()
    )
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")

    update_data = announcement_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(announcement, key, value)

    db.commit()
    db.refresh(announcement)
    return announcement


@router.delete("/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    """删除公告"""
    announcement = (
        db.query(Announcement).filter(Announcement.id == announcement_id).first()
    )
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")

    db.delete(announcement)
    db.commit()
    return {"message": "删除成功"}
