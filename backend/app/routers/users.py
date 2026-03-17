"""
用户管理路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.routers.auth import (
    get_password_hash,
    oauth2_scheme,
    jwt,
    SECRET_KEY,
    ALGORITHM,
)
from jose import JWTError

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "user"
    is_active: Optional[bool] = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True


def get_current_admin_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """获取当前管理员用户"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role != "admin":
            raise HTTPException(status_code=403, detail="权限不足")
    except JWTError:
        raise HTTPException(status_code=401, detail="令牌验证失败")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """创建用户（仅管理员）"""
    # 检查用户名是否存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 将空字符串转换为 None
    email = user_data.email if user_data.email and user_data.email.strip() else None
    phone = user_data.phone if user_data.phone and user_data.phone.strip() else None

    # 创建用户
    db_user = User(
        username=user_data.username,
        password=get_password_hash(user_data.password),
        email=email,
        phone=phone,
        role=user_data.role,
        is_active=user_data.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """删除用户（仅管理员）"""
    # 不能删除 admin 账号
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if user.username == "admin":
        raise HTTPException(status_code=403, detail="不能删除 admin 账号")

    db.delete(user)
    db.commit()
    return {"message": "删除成功"}


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """获取用户列表（仅管理员）"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """获取用户详情（仅管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """更新用户信息（仅管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 不能修改 admin 账号的用户名
    if user.username == "admin":
        raise HTTPException(status_code=403, detail="不能修改 admin 账号")

    # 将空字符串转换为 None
    if user_data.email is not None:
        user.email = user_data.email if user_data.email.strip() else None
    if user_data.phone is not None:
        user.phone = user_data.phone if user_data.phone.strip() else None
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    if user_data.password is not None and user_data.password:
        user.password = get_password_hash(user_data.password)

    db.commit()
    db.refresh(user)
    return user
