"""
租赁合同管理路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import json
import re
from jose import JWTError

from app.database import get_db
from app.models.lease import Lease
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


class LeaseCreate(BaseModel):
    tenant_id: int = Field(..., gt=0, description="租客 ID")
    landlord_id: int = Field(..., gt=0, description="房东 ID")
    house_id: int = Field(..., gt=0, description="房屋 ID")
    lease_years: int = Field(..., gt=0, le=99, description="租赁期限（年）")
    start_date: str = Field(..., description="起租日期")
    end_date: str = Field(..., description="终止日期")
    monthly_rent: float = Field(..., gt=0, description="月租金")
    payment_type: str = Field(..., max_length=20, description="支付方式")
    deposit: float = Field(..., ge=0, description="保证金")
    water_fee: Optional[str] = Field(None, max_length=20, description="水费承担方")
    electricity_fee: Optional[str] = Field(
        None, max_length=20, description="电费承担方"
    )
    gas_fee: Optional[str] = Field(None, max_length=20, description="燃气费承担方")
    property_fee: Optional[str] = Field(None, max_length=20, description="物业费承担方")
    furniture_list: Optional[str] = Field(None, description="家具电器清单")

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """验证日期格式"""
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("日期格式必须为 YYYY-MM-DD")

    def to_dict(self):
        """转换为字典，并将日期字符串转为 datetime 对象"""
        from datetime import datetime

        data = self.model_dump()
        # 将日期字符串转为 datetime 对象
        data["start_date"] = datetime.strptime(self.start_date, "%Y-%m-%d")
        data["end_date"] = datetime.strptime(self.end_date, "%Y-%m-%d")
        return data


class LeaseUpdate(BaseModel):
    lease_years: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    monthly_rent: Optional[float] = None
    payment_type: Optional[str] = None
    deposit: Optional[float] = None
    water_fee: Optional[str] = None
    electricity_fee: Optional[str] = None
    gas_fee: Optional[str] = None
    property_fee: Optional[str] = None
    furniture_list: Optional[str] = None
    status: Optional[str] = None


class LeaseResponse(BaseModel):
    id: int
    tenant_id: int
    landlord_id: int
    house_id: int
    lease_years: int
    start_date: datetime
    end_date: datetime
    monthly_rent: float
    payment_type: str
    deposit: float
    water_fee: Optional[str]
    electricity_fee: Optional[str]
    gas_fee: Optional[str]
    property_fee: Optional[str]
    furniture_list: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    # 关联信息
    house_address: Optional[str] = None
    tenant_name: Optional[str] = None
    tenant_phone: Optional[str] = None

    class Config:
        from_attributes = True


class LeaseWithRelationsResponse(BaseModel):
    id: int
    tenant_id: Optional[int] = None
    landlord_id: Optional[int] = None
    house_id: Optional[int] = None
    lease_years: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    monthly_rent: Optional[float] = None
    payment_type: Optional[str] = None
    deposit: Optional[float] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # 房屋信息
    house_address: Optional[str] = None
    house_area: Optional[float] = None
    house_usage: Optional[str] = None
    house_property_cert: Optional[str] = None
    # 租客信息
    tenant_name: Optional[str] = None
    tenant_phone: Optional[str] = None
    tenant_id_card: Optional[str] = None
    tenant_address: Optional[str] = None
    # 房东信息
    landlord_name: Optional[str] = None
    landlord_phone: Optional[str] = None
    landlord_id_card: Optional[str] = None
    landlord_address: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=LeaseResponse)
def create_lease(
    lease_data: LeaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建租赁合同"""
    db_lease = Lease(**lease_data.to_dict(), user_id=current_user.id)
    db.add(db_lease)
    db.commit()
    db.refresh(db_lease)
    return db_lease


@router.get("/", response_model=List[LeaseWithRelationsResponse])
def get_leases(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取租赁合同列表（时间倒序）"""
    # 限制最大分页数量
    if limit > 100:
        limit = 100

    from sqlalchemy.orm import joinedload
    from app.models.house import House
    from app.models.tenant import Tenant
    from app.models.landlord import Landlord

    leases = (
        db.query(Lease)
        .options(
            joinedload(Lease.house),
            joinedload(Lease.tenant),
            joinedload(Lease.landlord),
        )
        .filter(Lease.user_id == current_user.id)
        .order_by(Lease.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # 转换为包含关联信息的响应
    result = []
    for lease in leases:
        lease_dict = {
            "id": lease.id,
            "tenant_id": lease.tenant_id,
            "landlord_id": lease.landlord_id,
            "house_id": lease.house_id,
            "lease_years": lease.lease_years,
            "start_date": lease.start_date,
            "end_date": lease.end_date,
            "monthly_rent": lease.monthly_rent,
            "payment_type": lease.payment_type,
            "deposit": lease.deposit,
            "status": lease.status,
            "created_at": lease.created_at,
            "updated_at": lease.updated_at,
            # 房屋信息
            "house_address": lease.house.address if lease.house else None,
            "house_area": lease.house.area if lease.house else None,
            "house_usage": lease.house.usage if lease.house else None,
            "house_property_cert": lease.house.property_cert if lease.house else None,
            # 租客信息
            "tenant_name": lease.tenant.name if lease.tenant else None,
            "tenant_phone": lease.tenant.phone if lease.tenant else None,
            "tenant_id_card": lease.tenant.id_card if lease.tenant else None,
            "tenant_address": lease.tenant.address if lease.tenant else None,
            # 房东信息
            "landlord_name": lease.landlord.name if lease.landlord else None,
            "landlord_phone": lease.landlord.phone if lease.landlord else None,
            "landlord_id_card": lease.landlord.id_card if lease.landlord else None,
            "landlord_address": lease.landlord.address if lease.landlord else None,
        }
        result.append(LeaseWithRelationsResponse(**lease_dict))

    return result


@router.get("/expiring", response_model=List[LeaseWithRelationsResponse])
def get_expiring_leases(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """获取 7 天内到期的租赁合同"""
    from datetime import timedelta
    from sqlalchemy.orm import joinedload
    from app.models.house import House
    from app.models.tenant import Tenant
    from app.models.landlord import Landlord

    now = datetime.now()
    seven_days_later = now + timedelta(days=7)

    leases = (
        db.query(Lease)
        .options(
            joinedload(Lease.house),
            joinedload(Lease.tenant),
            joinedload(Lease.landlord),
        )
        .filter(
            Lease.user_id == current_user.id,
            Lease.status == "active",
            Lease.end_date != None,
            Lease.end_date >= now,
            Lease.end_date <= seven_days_later,
        )
        .all()
    )

    # 转换为包含关联信息的响应
    result = []
    for lease in leases:
        lease_dict = {
            "id": lease.id,
            "tenant_id": lease.tenant_id,
            "landlord_id": lease.landlord_id,
            "house_id": lease.house_id,
            "lease_years": lease.lease_years,
            "start_date": lease.start_date,
            "end_date": lease.end_date,
            "monthly_rent": lease.monthly_rent,
            "payment_type": lease.payment_type,
            "deposit": lease.deposit,
            "status": lease.status,
            "created_at": lease.created_at,
            "updated_at": lease.updated_at,
            # 房屋信息
            "house_address": lease.house.address if lease.house else None,
            "house_area": lease.house.area if lease.house else None,
            "house_usage": lease.house.usage if lease.house else None,
            "house_property_cert": lease.house.property_cert if lease.house else None,
            # 租客信息
            "tenant_name": lease.tenant.name if lease.tenant else None,
            "tenant_phone": lease.tenant.phone if lease.tenant else None,
            "tenant_id_card": lease.tenant.id_card if lease.tenant else None,
            "tenant_address": lease.tenant.address if lease.tenant else None,
            # 房东信息
            "landlord_name": lease.landlord.name if lease.landlord else None,
            "landlord_phone": lease.landlord.phone if lease.landlord else None,
            "landlord_id_card": lease.landlord.id_card if lease.landlord else None,
            "landlord_address": lease.landlord.address if lease.landlord else None,
        }
        result.append(LeaseWithRelationsResponse(**lease_dict))

    return result


@router.get("/overdue", response_model=List[LeaseWithRelationsResponse])
def get_overdue_leases(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """获取已超期的租赁合同"""
    from sqlalchemy.orm import joinedload
    from app.models.house import House
    from app.models.tenant import Tenant
    from app.models.landlord import Landlord

    now = datetime.now()

    leases = (
        db.query(Lease)
        .options(
            joinedload(Lease.house),
            joinedload(Lease.tenant),
            joinedload(Lease.landlord),
        )
        .filter(
            Lease.user_id == current_user.id,
            Lease.status == "active",
            Lease.end_date != None,
            Lease.end_date < now,
        )
        .all()
    )

    # 转换为包含关联信息的响应
    result = []
    for lease in leases:
        lease_dict = {
            "id": lease.id,
            "tenant_id": lease.tenant_id,
            "landlord_id": lease.landlord_id,
            "house_id": lease.house_id,
            "lease_years": lease.lease_years,
            "start_date": lease.start_date,
            "end_date": lease.end_date,
            "monthly_rent": lease.monthly_rent,
            "payment_type": lease.payment_type,
            "deposit": lease.deposit,
            "status": lease.status,
            "created_at": lease.created_at,
            "updated_at": lease.updated_at,
            # 房屋信息
            "house_address": lease.house.address if lease.house else None,
            "house_area": lease.house.area if lease.house else None,
            "house_usage": lease.house.usage if lease.house else None,
            "house_property_cert": lease.house.property_cert if lease.house else None,
            # 租客信息
            "tenant_name": lease.tenant.name if lease.tenant else None,
            "tenant_phone": lease.tenant.phone if lease.tenant else None,
            "tenant_id_card": lease.tenant.id_card if lease.tenant else None,
            "tenant_address": lease.tenant.address if lease.tenant else None,
            # 房东信息
            "landlord_name": lease.landlord.name if lease.landlord else None,
            "landlord_phone": lease.landlord.phone if lease.landlord else None,
            "landlord_id_card": lease.landlord.id_card if lease.landlord else None,
            "landlord_address": lease.landlord.address if lease.landlord else None,
        }
        result.append(LeaseWithRelationsResponse(**lease_dict))

    return result


@router.get("/{lease_id}", response_model=LeaseWithRelationsResponse)
def get_lease(
    lease_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取租赁合同详情"""
    from sqlalchemy.orm import joinedload
    from app.models.house import House
    from app.models.tenant import Tenant
    from app.models.landlord import Landlord

    lease = (
        db.query(Lease)
        .options(
            joinedload(Lease.house),
            joinedload(Lease.tenant),
            joinedload(Lease.landlord),
        )
        .filter(Lease.id == lease_id, Lease.user_id == current_user.id)
        .first()
    )

    if not lease:
        raise HTTPException(status_code=404, detail="租赁合同不存在")

    lease_dict = {
        "id": lease.id,
        "tenant_id": lease.tenant_id,
        "landlord_id": lease.landlord_id,
        "house_id": lease.house_id,
        "lease_years": lease.lease_years,
        "start_date": lease.start_date,
        "end_date": lease.end_date,
        "monthly_rent": lease.monthly_rent,
        "payment_type": lease.payment_type,
        "deposit": lease.deposit,
        "status": lease.status,
        "created_at": lease.created_at,
        "updated_at": lease.updated_at,
        # 房屋信息
        "house_address": lease.house.address if lease.house else None,
        "house_area": lease.house.area if lease.house else None,
        "house_usage": lease.house.usage if lease.house else None,
        "house_property_cert": lease.house.property_cert if lease.house else None,
        # 租客信息
        "tenant_name": lease.tenant.name if lease.tenant else None,
        "tenant_phone": lease.tenant.phone if lease.tenant else None,
        "tenant_id_card": lease.tenant.id_card if lease.tenant else None,
        "tenant_address": lease.tenant.address if lease.tenant else None,
        # 房东信息
        "landlord_name": lease.landlord.name if lease.landlord else None,
        "landlord_phone": lease.landlord.phone if lease.landlord else None,
        "landlord_id_card": lease.landlord.id_card if lease.landlord else None,
        "landlord_address": lease.landlord.address if lease.landlord else None,
    }
    return LeaseWithRelationsResponse(**lease_dict)


@router.post("/{lease_id}/export")
def export_lease(
    lease_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """导出租赁合同为 docx 文件"""
    import os
    from pathlib import Path
    from docx import Document
    from sqlalchemy.orm import joinedload
    from app.models.house import House
    from app.models.tenant import Tenant
    from app.models.landlord import Landlord

    lease = (
        db.query(Lease)
        .options(
            joinedload(Lease.house),
            joinedload(Lease.tenant),
            joinedload(Lease.landlord),
        )
        .filter(Lease.id == lease_id, Lease.user_id == current_user.id)
        .first()
    )

    if not lease:
        raise HTTPException(status_code=404, detail="租赁合同不存在")

    # 获取项目根目录 (E:/pyStudy/zulin)
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    out_dir = base_dir / "out"
    out_dir.mkdir(exist_ok=True)

    output_path = out_dir / f"{lease_id}.docx"

    # 如果文件已存在，先删除
    if output_path.exists():
        output_path.unlink()

    # 读取模板
    template_path = base_dir / "ht.docx"
    if not template_path.exists():
        raise HTTPException(status_code=500, detail="模板文件不存在")

    doc = Document(str(template_path))

    # 替换模板中的占位符
    for para in doc.paragraphs:
        text = para.text

        # 出租方 (甲方) 信息
        if lease.landlord:
            if "出租方 (甲方)" in text:
                para.text = f"出租方 (甲方): {lease.landlord.name}"
            elif "身份证" in text and len(text) < 50:
                para.text = f"身份证：{lease.landlord.id_card}"
            elif "电话" in text and len(text) < 30:
                para.text = f"电话：{lease.landlord.phone}"
            elif "地址" in text and len(text) < 100:
                para.text = f"地址：{lease.landlord.address}"

        # 承租方 (乙方) 信息
        if lease.tenant:
            if "承租方 (乙方)" in text:
                para.text = f"承租方 (乙方): {lease.tenant.name}"
            elif "身份证" in text and len(text) < 50:
                para.text = f"身份证：{lease.tenant.id_card}"
            elif "电话" in text and len(text) < 30:
                para.text = f"电话：{lease.tenant.phone}"
            elif "地址" in text and len(text) < 100:
                para.text = f"地址：{lease.tenant.address}"

        # 房屋信息
        if lease.house and lease.house.address:
            if "地址" in text and len(text) < 100:
                para.text = f"地址：{lease.house.address}"

        # 租赁信息
        if "元" in text and "月" in text:
            para.text = text.replace("元", f"{lease.monthly_rent}元")
        if "保证金" in text:
            para.text = f"保证金：{lease.deposit} 元"
        if "租赁期限" in text:
            para.text = f"租赁期限：{lease.lease_years}年"
        if lease.start_date and "起租" in text:
            start_date_str = lease.start_date.strftime("%Y年%m月%d日")
            para.text = f"起租日期：{start_date_str}"
        if lease.end_date and "到期" in text:
            end_date_str = lease.end_date.strftime("%Y年%m月%d日")
            para.text = f"到期日期：{end_date_str}"

    # 保存文件
    doc.save(str(output_path))

    return {
        "message": "导出成功",
        "file_path": str(output_path),
        "file_name": f"{lease_id}.docx",
    }


@router.put("/{lease_id}", response_model=LeaseResponse)
def update_lease(
    lease_id: int,
    lease_data: LeaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新租赁合同信息"""
    lease = (
        db.query(Lease)
        .filter(Lease.id == lease_id, Lease.user_id == current_user.id)
        .first()
    )
    if not lease:
        raise HTTPException(status_code=404, detail="租赁合同不存在")

    update_data = lease_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lease, key, value)

    db.commit()
    db.refresh(lease)
    return lease


@router.delete("/{lease_id}")
def delete_lease(
    lease_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除租赁合同"""
    lease = (
        db.query(Lease)
        .filter(Lease.id == lease_id, Lease.user_id == current_user.id)
        .first()
    )
    if not lease:
        raise HTTPException(status_code=404, detail="租赁合同不存在")

    db.delete(lease)
    db.commit()
    return {"message": "删除成功"}
