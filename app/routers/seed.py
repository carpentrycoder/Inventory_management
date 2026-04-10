"""
Seed Router — Generate sample data for development/testing
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import models
import random
from faker import Faker

fake = Faker()

router = APIRouter(prefix="/seed", tags=["Seed"])


@router.post("/seed-data")
async def seed_data(
    count: int = 5,  # 👈 number of records you want
    db: AsyncSession = Depends(get_db)
):
    try:
        categories = []
        suppliers = []
        items = []

        # 🔹 1. Create Categories
        for _ in range(count):
            category = models.Category(
                name=fake.unique.word().capitalize(),
                description=fake.sentence()
            )
            db.add(category)
            categories.append(category)

        await db.commit()

        for c in categories:
            await db.refresh(c)

        # 🔹 2. Create Suppliers
        for _ in range(count):
            supplier = models.Supplier(
                name=fake.company(),
                contact_info=fake.phone_number(),
                address=fake.city()
            )
            db.add(supplier)
            suppliers.append(supplier)

        await db.commit()

        for s in suppliers:
            await db.refresh(s)

        # 🔹 3. Create Items
        for _ in range(count * 2):  # more items
            item = models.Item(
                name=fake.word().capitalize(),
                description=fake.sentence(),
                quantity=random.randint(1, 100),
                price=random.randint(100, 100000),
                category_id=random.choice(categories).id,
                supplier_id=random.choice(suppliers).id
            )
            db.add(item)
            items.append(item)

        await db.commit()

        for i in items:
            await db.refresh(i)

        # 🔹 4. Purchases
        purchases = []
        for _ in range(count):
            purchase = models.Purchase(
                supplier_id=random.choice(suppliers).id,
                total_cost=random.randint(1000, 200000)
            )
            db.add(purchase)
            purchases.append(purchase)

        await db.commit()

        for p in purchases:
            await db.refresh(p)

        # 🔹 5. Dispatches
        dispatches = []
        for _ in range(count):
            dispatch = models.Dispatch(
                customer_name=fake.name(),
                purpose=fake.word()
            )
            db.add(dispatch)
            dispatches.append(dispatch)

        await db.commit()

        for d in dispatches:
            await db.refresh(d)

        # 🔹 6. Stock Transactions
        for _ in range(count * 3):
            txn = models.StockTransaction(
                item_id=random.choice(items).id,
                change_type=random.choice(["IN", "OUT"]),
                quantity=random.randint(1, 20),
                purchase_id=random.choice(purchases).id if random.random() > 0.5 else None,
                dispatch_id=random.choice(dispatches).id if random.random() > 0.5 else None,
                notes=fake.sentence()
            )
            db.add(txn)

        await db.commit()

        return {
            "message": f"✅ {count} sample data sets inserted successfully 🚀"
        }

    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
