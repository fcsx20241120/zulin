"""
房屋管理路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from jose import JWTError

from app.database import get_db
from app.models.house import House
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


class HouseCreate(BaseModel):
    address: str
    area: Optional[float] = None
    usage: Optional[str] = None
    property_cert: Optional[str] = None


class HouseUpdate(BaseModel):
    address: Optional[str] = None
    area: Optional[float] = None
    usage: Optional[str] = None
    property_cert: Optional[str] = None


class HouseResponse(BaseModel):
    id: int
    address: str
    area: Optional[float]
    usage: Optional[str]
    property_cert: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=HouseResponse)
def create_house(
    house_data: HouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建房屋"""
    db_house = House(**house_data.model_dump(), user_id=current_user.id)
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house


@router.get("/", response_model=List[HouseResponse])
def get_houses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取房屋列表（时间倒序）"""
    # 管理员能看到所有数据，普通用户只能看自己的
    query = db.query(House)
    if not is_admin(current_user):
        query = query.filter(House.user_id == current_user.id)

    houses = query.order_by(House.created_at.desc()).offset(skip).limit(limit).all()
    return houses


@router.get("/{house_id}", response_model=HouseResponse)
def get_house(
    house_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取房屋详情"""
    # 管理员能看到所有数据，普通用户只能看自己的
    query = db.query(House)
    if not is_admin(current_user):
        query = query.filter(House.id == house_id, House.user_id == current_user.id)
    else:
        query = query.filter(House.id == house_id)

    house = query.first()
    if not house:
        raise HTTPException(status_code=404, detail="房屋不存在")
    return house


@router.put("/{house_id}", response_model=HouseResponse)
def update_house(
    house_id: int,
    house_data: HouseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新房屋信息"""
    # 管理员能操作所有数据，普通用户只能操作自己的
    query = db.query(House)
    if not is_admin(current_user):
        query = query.filter(House.id == house_id, House.user_id == current_user.id)
    else:
        query = query.filter(House.id == house_id)

    house = query.first()
    if not house:
        raise HTTPException(status_code=404, detail="房屋不存在")

    update_data = house_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(house, key, value)

    db.commit()
    db.refresh(house)
    return house


@router.delete("/{house_id}")
def delete_house(
    house_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除房屋"""
    # 管理员能操作所有数据，普通用户只能操作自己的
    query = db.query(House)
    if not is_admin(current_user):
        query = query.filter(House.id == house_id, House.user_id == current_user.id)
    else:
        query = query.filter(House.id == house_id)

    house = query.first()
    if not house:
        raise HTTPException(status_code=404, detail="房屋不存在")

    db.delete(house)
    db.commit()
    return {"message": "删除成功"}
