"""
模拟数据生成脚本
为 user_id=2 生成 10 套完整的租赁数据（租客、房东、房屋、合同）
"""

import json
import os
from datetime import datetime

from app.database import SessionLocal, engine, Base
from app.models.tenant import Tenant
from app.models.landlord import Landlord
from app.models.house import House
from app.models.lease import Lease
from app.models.announcement import Announcement


def load_seed_data():
    """加载种子数据"""
    seed_file = os.path.join(os.path.dirname(__file__), "demo", "seed_data.json")
    with open(seed_file, "r", encoding="utf-8") as f:
        return json.load(f)


def create_demo_data(user_id: int = 2):
    """创建模拟数据"""
    db = SessionLocal()
    try:
        data = load_seed_data()

        print("=" * 60)
        print(f"开始为 user_id={user_id} 创建模拟数据")
        print("=" * 60)

        tenants = []
        landlords = []
        houses = []

        for tenant_data in data["tenants"]:
            tenant = Tenant(
                user_id=user_id,
                **tenant_data,
            )
            db.add(tenant)
            tenants.append(tenant)
        db.commit()
        print(f"[OK] 已创建 {len(tenants)} 个租客")

        for landlord_data in data["landlords"]:
            landlord = Landlord(
                user_id=user_id,
                **landlord_data,
            )
            db.add(landlord)
            landlords.append(landlord)
        db.commit()
        print(f"[OK] 已创建 {len(landlords)} 个房东")

        for house_data in data["houses"]:
            house = House(
                user_id=user_id,
                **house_data,
            )
            db.add(house)
            houses.append(house)
        db.commit()
        print(f"[OK] 已创建 {len(houses)} 套房屋")

        for lease_data in data["leases"]:
            tenant_idx = lease_data.pop("tenant_idx")
            landlord_idx = lease_data.pop("landlord_idx")
            house_idx = lease_data.pop("house_idx")

            lease = Lease(
                user_id=user_id,
                tenant_id=tenants[tenant_idx].id,
                landlord_id=landlords[landlord_idx].id,
                house_id=houses[house_idx].id,
                **lease_data,
            )
            db.add(lease)
        db.commit()
        print(f"[OK] 已创建 {len(data['leases'])} 份租赁合同")

        for ann_data in data["announcements"]:
            announcement = Announcement(**ann_data)
            db.add(announcement)
        db.commit()
        print(f"[OK] 已创建 {len(data['announcements'])} 条公告")

        print("=" * 60)
        print("模拟数据创建完成！")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"[ERROR] 创建数据时出错：{e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data(user_id=2)
