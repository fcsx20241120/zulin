"""
房东管理路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from jose import JWTError

from app.database import get_db
from app.models.landlord import Landlord
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


class LandlordCreate(BaseModel):
    name: str
    address: Optional[str] = None
    id_card: Optional[str] = None
    phone: Optional[str] = None


class LandlordUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    id_card: Optional[str] = None
    phone: Optional[str] = None


class LandlordResponse(BaseModel):
    id: int
    name: str
    address: Optional[str]
    id_card: Optional[str]
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=LandlordResponse)
def create_landlord(
    landlord_data: LandlordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建房东"""
    db_landlord = Landlord(**landlord_data.model_dump(), user_id=current_user.id)
    db.add(db_landlord)
    db.commit()
    db.refresh(db_landlord)
    return db_landlord


@router.get("/", response_model=List[LandlordResponse])
def get_landlords(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取房东列表（时间倒序）"""
    # 管理员能看到所有数据，普通用户只能看自己的
    query = db.query(Landlord)
    if not is_admin(current_user):
        query = query.filter(Landlord.user_id == current_user.id)

    landlords = (
        query.order_by(Landlord.created_at.desc()).offset(skip).limit(limit).all()
    )
    return landlords


@router.get("/{landlord_id}", response_model=LandlordResponse)
def get_landlord(
    landlord_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取房东详情"""
    # 管理员能看到所有数据，普通用户只能看自己的
    query = db.query(Landlord)
    if not is_admin(current_user):
        query = query.filter(
            Landlord.id == landlord_id, Landlord.user_id == current_user.id
        )
    else:
        query = query.filter(Landlord.id == landlord_id)

    landlord = query.first()
    if not landlord:
        raise HTTPException(status_code=404, detail="房东不存在")
    return landlord


@router.put("/{landlord_id}", response_model=LandlordResponse)
def update_landlord(
    landlord_id: int,
    landlord_data: LandlordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新房东信息"""
    # 管理员能操作所有数据，普通用户只能操作自己的
    query = db.query(Landlord)
    if not is_admin(current_user):
        query = query.filter(
            Landlord.id == landlord_id, Landlord.user_id == current_user.id
        )
    else:
        query = query.filter(Landlord.id == landlord_id)

    landlord = query.first()
    if not landlord:
        raise HTTPException(status_code=404, detail="房东不存在")

    update_data = landlord_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(landlord, key, value)

    db.commit()
    db.refresh(landlord)
    return landlord


@router.delete("/{landlord_id}")
def delete_landlord(
    landlord_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除房东"""
    # 管理员能操作所有数据，普通用户只能操作自己的
    query = db.query(Landlord)
    if not is_admin(current_user):
        query = query.filter(
            Landlord.id == landlord_id, Landlord.user_id == current_user.id
        )
    else:
        query = query.filter(Landlord.id == landlord_id)

    landlord = query.first()
    if not landlord:
        raise HTTPException(status_code=404, detail="房东不存在")

    db.delete(landlord)
    db.commit()
    return {"message": "删除成功"}
