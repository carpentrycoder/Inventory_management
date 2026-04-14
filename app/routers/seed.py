"""
Seed Router — Generate sample data for development/testing
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine
from app import models
import random
from faker import Faker
import os
import asyncio
from seed_data import seed_data

fake = Faker()

router = APIRouter(prefix="/seed", tags=["Seed"])


@router.post("/reset-db")
async def reset_database():
    """Reset the database: drop all tables, recreate, and seed data"""
    try:
        # Drop all tables
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.drop_all)
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        
        # Seed data
        await seed_data()
        
        return {"message": "Database reset and seeded successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.post("/seed-data")
async def seed_data(db: AsyncSession = Depends(get_db)):
    try:
        # ==============================
        # 🔹 1. Categories
        # ==============================
        category_data = [
            "Fresh Food",
            "Packaged Food",
            "Frozen & Ready Food",
            "Beverages",
            "Bathroom & Personal Care",
            "Cleaning Supplies",
            "Packaging & Disposable Items",
            "Utensils & Service Items"
        ]

        categories = []
        for name in category_data:
            cat = models.Category(name=name, description=f"{name} items")
            db.add(cat)
            categories.append(cat)

        await db.commit()
        for c in categories:
            await db.refresh(c)

        category_map = {c.name: c.id for c in categories}

        # ==============================
        # 🔹 2. Suppliers
        # ==============================
        supplier_data = [
            ("FreshFarm Suppliers", "Ramesh Patil", "freshfarm@gmail.com", "9876543210", "Navi Mumbai"),
            ("DailyNeeds Distributors", "Priya Shah", "dailyneeds@gmail.com", "9823456781", "Thane"),
            ("CoolStorage Pvt Ltd", "Amit Verma", "coolstorage@gmail.com", "9811122233", "Pune"),
            ("Beverage Hub", "Suresh Yadav", "beveragehub@gmail.com", "9898989898", "Mumbai"),
            ("Hygiene World", "Neha Joshi", "hygiene@gmail.com", "9765432109", "Dombivli"),
            ("CleanPro Supplies", "Akash Mehta", "cleanpro@gmail.com", "9700000001", "Mumbai"),
            ("PackIt Solutions", "Rahul Jain", "packit@gmail.com", "9755555555", "Bhiwandi"),
            ("KitchenServe India", "Vikram Singh", "kitchenserve@gmail.com", "9696969696", "Mumbai"),
        ]

        suppliers = []
        for s in supplier_data:
            sup = models.Supplier(
                name=s[0],
                contact_person=s[1],
                email=s[2],
                phone=s[3],
                contact_info=s[3],
                address=s[4]
            )
            db.add(sup)
            suppliers.append(sup)

        await db.commit()
        for s in suppliers:
            await db.refresh(s)

        supplier_map = {s.name: s.id for s in suppliers}

        # ==============================
        # 🔹 3. Items (11 per category)
        # ==============================
        items_data = {
            "Fresh Food": ["Apple","Banana","Mango","Tomato","Potato","Onion","Milk","Eggs","Chicken","Fish","Paneer"],
            "Packaged Food": ["Rice","Wheat Flour","Pasta","Lentils","Cornflakes","Canned Beans","Tomato Ketchup","Cooking Oil","Sugar","Baking Powder","Salt"],
            "Frozen & Ready Food": ["Ice Cream","Frozen Peas","Frozen Fries","Frozen Nuggets","Frozen Pizza","Bread","Cake","Biscuits","Muffins","Sandwich","Ready Meal"],
            "Beverages": ["Coca Cola","Pepsi","Orange Juice","Apple Juice","Energy Drink","Tea","Coffee","Green Tea","Cold Coffee","Soda","Mineral Water"],
            "Bathroom & Personal Care": ["Soap","Shampoo","Conditioner","Toothpaste","Toothbrush","Face Wash","Body Wash","Hand Wash","Shaving Cream","Razor","Sanitary Pads"],
            "Cleaning Supplies": ["Detergent Powder","Liquid Detergent","Floor Cleaner","Glass Cleaner","Toilet Cleaner","Disinfectant Spray","Sanitizer","Bleach","Scrub Pads","Mop","Trash Bags"],
            "Packaging & Disposable Items": ["Plastic Containers","Paper Plates","Paper Cups","Napkins","Straws","Aluminium Foil","Cling Wrap","Takeaway Boxes","Coffee Cup Lids","Plastic Spoons","Garbage Bags"],
            "Utensils & Service Items": ["Glass","Plate","Bowl","Spoon","Fork","Knife","Serving Tray","Jug","Tablecloth","Cooking Pan","Cooking Pot"]
        }

        category_supplier_map = {
            "Fresh Food": "FreshFarm Suppliers",
            "Packaged Food": "DailyNeeds Distributors",
            "Frozen & Ready Food": "CoolStorage Pvt Ltd",
            "Beverages": "Beverage Hub",
            "Bathroom & Personal Care": "Hygiene World",
            "Cleaning Supplies": "CleanPro Supplies",
            "Packaging & Disposable Items": "PackIt Solutions",
            "Utensils & Service Items": "KitchenServe India"
        }

        items = []
        sku_counter = 1000

        for category, item_list in items_data.items():
            for item_name in item_list:
                sku_counter += 1

                quantity = random.randint(10, 200)
                price = random.randint(50, 5000)
                total_price = quantity * price  # Calculate total_price separately

                item = models.Item(
                    name=item_name,
                    description=f"{item_name} ({category})",
                    sku=f"SKU{sku_counter}",
                    quantity=quantity,
                    price=price,
                    total_price=total_price,  # Use calculated total_price
                    category_id=category_map[category],
                    supplier_id=supplier_map[category_supplier_map[category]]
                )
                db.add(item)
                items.append(item)

        await db.commit()
        for i in items:
            await db.refresh(i)

        # ==============================
        # 🔹 4. Purchases
        # ==============================
        purchases = []
        for s in suppliers:
            purchase = models.Purchase(
                supplier_id=s.id,
                total_cost=random.randint(5000, 50000)
            )
            db.add(purchase)
            purchases.append(purchase)

        await db.commit()
        for p in purchases:
            await db.refresh(p)

        # ==============================
        # 🔹 5. Dispatches
        # ==============================
        dispatches = []
        for _ in range(8):
            d = models.Dispatch(
                customer_name=fake.name(),
                purpose="Retail Sale"
            )
            db.add(d)
            dispatches.append(d)

        await db.commit()
        for d in dispatches:
            await db.refresh(d)

        # ==============================
        # 🔹 6. Stock Transactions
        # ==============================
        for item in items:
            txn = models.StockTransaction(
                item_id=item.id,
                change_type=random.choice(["IN", "OUT"]),
                quantity=random.randint(1, 20),
                purchase_id=random.choice(purchases).id,
                dispatch_id=random.choice(dispatches).id,
                notes="Auto generated transaction"
            )
            db.add(txn)

        await db.commit()

        return {"message": "✅ Structured inventory data inserted successfully 🚀"}

    except Exception as e:
        await db.rollback()
        return {"error": str(e)}


@router.post("/bulk-stock-update")
async def bulk_stock_update(
    updates: list[dict],  # List of updates with item_id and quantity
    db: AsyncSession = Depends(get_db)
):
    """Update stock quantities for multiple items in bulk."""
    try:
        for update in updates:
            item = await db.get(models.Item, update["item_id"])
            if item:
                item.quantity = update.get("quantity", item.quantity)
                db.add(item)

        await db.commit()
        return {"message": "Bulk stock update successful"}
    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
