"""
租客管理路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime
import re
from jose import JWTError

from app.database import get_db
from app.models.tenant import Tenant
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


def validate_id_card(id_card: Optional[str]) -> Optional[str]:
    """验证身份证号格式"""
    if id_card is None:
        return None
    pattern = r"^\d{17}[\dXx]$|^\d{15}$"
    if not re.match(pattern, id_card):
        raise HTTPException(status_code=400, detail="身份证号格式不正确")
    return id_card


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="姓名")
    address: Optional[str] = Field(None, max_length=255, description="地址")
    id_card: Optional[str] = Field(None, max_length=50, description="身份证号")
    phone: Optional[str] = Field(None, max_length=20, description="电话")


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    id_card: Optional[str] = None
    phone: Optional[str] = None


class TenantResponse(BaseModel):
    id: int
    name: str
    address: Optional[str]
    id_card: Optional[str]
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=TenantResponse)
def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建租客"""
    # 验证身份证号
    if tenant_data.id_card:
        validate_id_card(tenant_data.id_card)

    db_tenant = Tenant(**tenant_data.model_dump(), user_id=current_user.id)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


@router.get("/", response_model=List[TenantResponse])
def get_tenants(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取租客列表（时间倒序）"""
    # 限制最大分页数量
    if limit > 100:
        limit = 100

    # 管理员能看到所有数据，普通用户只能看自己的
    query = db.query(Tenant)
    if not is_admin(current_user):
        query = query.filter(Tenant.user_id == current_user.id)

    tenants = query.order_by(Tenant.created_at.desc()).offset(skip).limit(limit).all()
    return tenants


@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取租客详情"""
    # 管理员能看到所有数据，普通用户只能看自己的
    query = db.query(Tenant)
    if not is_admin(current_user):
        query = query.filter(Tenant.id == tenant_id, Tenant.user_id == current_user.id)
    else:
        query = query.filter(Tenant.id == tenant_id)

    tenant = query.first()
    if not tenant:
        raise HTTPException(status_code=404, detail="租客不存在")
    return tenant


@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新租客信息"""
    # 管理员能操作所有数据，普通用户只能操作自己的
    query = db.query(Tenant)
    if not is_admin(current_user):
        query = query.filter(Tenant.id == tenant_id, Tenant.user_id == current_user.id)
    else:
        query = query.filter(Tenant.id == tenant_id)

    tenant = query.first()
    if not tenant:
        raise HTTPException(status_code=404, detail="租客不存在")

    update_data = tenant_data.model_dump(exclude_unset=True)

    # 验证身份证号
    if update_data.get("id_card"):
        validate_id_card(update_data["id_card"])

    for key, value in update_data.items():
        setattr(tenant, key, value)

    db.commit()
    db.refresh(tenant)
    return tenant


@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除租客"""
    # 管理员能操作所有数据，普通用户只能操作自己的
    query = db.query(Tenant)
    if not is_admin(current_user):
        query = query.filter(Tenant.id == tenant_id, Tenant.user_id == current_user.id)
    else:
        query = query.filter(Tenant.id == tenant_id)

    tenant = query.first()
    if not tenant:
        raise HTTPException(status_code=404, detail="租客不存在")

    db.delete(tenant)
    db.commit()
    return {"message": "删除成功"}
