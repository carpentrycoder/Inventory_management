# app/routers/inventory.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from .. import crud, schemas, database, models

router = APIRouter(
    prefix="/inventory" \
    "",
    tags=["Inventory"]
)

get_db = database.get_db

# --------------------------
# CATEGORY ROUTES
# --------------------------
@router.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(db=db, category=category)

@router.get("/categories/", response_model=List[schemas.Category])
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db=db, skip=skip, limit=limit)

@router.get("/categories/{category_id}", response_model=schemas.Category)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    db_category = await crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/categories/{category_id}", response_model=schemas.Category)
async def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    db_category = await crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return await crud.update_category(
        db=db,
        category_id=category_id,
        category_update=category
    )

# --------------------------
# SUPPLIER ROUTES
# --------------------------
@router.post("/suppliers/", response_model=schemas.Supplier)
async def create_supplier(supplier: schemas.SupplierCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_supplier(db=db, supplier=supplier)

@router.get("/suppliers/", response_model=List[schemas.Supplier])
async def get_suppliers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_suppliers(db=db, skip=skip, limit=limit)

@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    db_supplier = await crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def update_supplier(
    supplier_id: int,
    supplier: schemas.SupplierCreate,
    db: AsyncSession = Depends(get_db)
):
    db_supplier = await crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return await crud.update_supplier(
        db=db,
        supplier_id=supplier_id,
        supplier_update=supplier
    )

# --------------------------
# ITEM ROUTES
# --------------------------
@router.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db=db, item=item)

@router.get("/items/", response_model=List[schemas.Item])
async def get_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_items(db=db, skip=skip, limit=limit)

@router.get("/items/{item_id}", response_model=schemas.Item)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(item_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    updated_item = await crud.update_item(db=db, item_id=item_id, item_update=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}", response_model=schemas.Item)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted_item = await crud.delete_item(db=db, item_id=item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item


# --------------------------  
# STOCK OPERATIONS
# --------------------------
@router.post("/stock-in")
async def stock_in(
    item_id: int,
    quantity: int,
    user_id: int,
    notes: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Add stock to an item"""
    # Check if item exists
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if user exists
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update item quantity
    item.quantity += quantity
    await db.commit()
    await db.refresh(item)
    
    # Create stock transaction
    transaction_data = schemas.StockTransactionCreate(
        item_id=item_id,
        change_type="IN",
        quantity=quantity,
        user_id=user_id,
        notes=notes
    )
    await crud.create_stock_transaction(db=db, transaction=transaction_data)
    
    return {"message": f"Added {quantity} units to {item.name}", "new_quantity": item.quantity}


@router.post("/stock-out")
async def stock_out(
    item_id: int,
    quantity: int,
    user_id: int,
    notes: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Remove stock from an item"""
    # Check if item exists
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if user exists
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if sufficient stock
    if item.quantity < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Update item quantity
    item.quantity -= quantity
    await db.commit()
    await db.refresh(item)
    
    # Create stock transaction
    transaction_data = schemas.StockTransactionCreate(
        item_id=item_id,
        change_type="OUT",
        quantity=quantity,
        user_id=user_id,
        notes=notes
    )
    await crud.create_stock_transaction(db=db, transaction=transaction_data)
    
    return {"message": f"Removed {quantity} units from {item.name}", "new_quantity": item.quantity}


# ===========================
# 🔥 ANALYTICS & DASHBOARDS
# ===========================

# 🔥 1. DASHBOARD SUMMARY API (MOST IMPORTANT)
@router.get("/dashboard/summary")
async def inventory_summary(db: AsyncSession = Depends(get_db)):
    """Get inventory overview with key metrics"""
    total_items = await db.scalar(select(func.count(models.Item.id)))
    total_stock = await db.scalar(select(func.sum(models.Item.quantity)))

    total_in = await db.scalar(
        select(func.sum(models.StockTransaction.quantity))
        .where(models.StockTransaction.change_type == "IN")
    )

    total_out = await db.scalar(
        select(func.sum(models.StockTransaction.quantity))
        .where(models.StockTransaction.change_type == "OUT")
    )

    return {
        "total_items": total_items or 0,
        "total_stock": total_stock or 0,
        "total_stock_in": total_in or 0,
        "total_stock_out": total_out or 0,
    }


# 🔥 2. STOCK MOVEMENT TIMELINE (UI FRIENDLY)
@router.get("/stock-movements")
async def stock_movements(db: AsyncSession = Depends(get_db)):
    """Get recent stock transactions with item details"""
    result = await db.execute(
        select(
            models.StockTransaction,
            models.Item.name.label("item_name"),
            models.Item.sku.label("sku")
        )
        .join(models.Item, models.Item.id == models.StockTransaction.item_id)
        .order_by(models.StockTransaction.timestamp.desc())
        .limit(50)
    )

    rows = result.all()

    return [
        {
            "transaction_id": t.StockTransaction.id,
            "item_id": t.StockTransaction.item_id,
            "item_name": t.item_name,
            "sku": t.sku,
            "type": t.StockTransaction.change_type,
            "quantity": t.StockTransaction.quantity,
            "timestamp": t.StockTransaction.timestamp,
            "notes": t.StockTransaction.notes,
        }
        for t in rows
    ]


# 🔥 3. ITEM STOCK LEDGER (VERY IMPORTANT FOR ERP UI)
@router.get("/items/{item_id}/ledger")
async def item_ledger(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get complete stock ledger for an item with running balance"""
    # Check if item exists
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    result = await db.execute(
        select(models.StockTransaction)
        .where(models.StockTransaction.item_id == item_id)
        .order_by(models.StockTransaction.timestamp.asc())
    )

    logs = result.scalars().all()

    balance = 0
    ledger = []

    for l in logs:  # compute running balance
        if l.change_type == "IN":
            balance += l.quantity
        else:
            balance -= l.quantity

        ledger.append({
            "id": l.id,
            "type": l.change_type,
            "qty": l.quantity,
            "timestamp": l.timestamp,
            "notes": l.notes,
            "running_balance": balance
        })

    return ledger


# 🔥 4. PURCHASE LIST (ENRICHED VERSION)
@router.get("/purchases")
async def get_purchases(db: AsyncSession = Depends(get_db)):
    """Get all purchases"""
    result = await db.execute(
        select(models.Purchase)
        .order_by(models.Purchase.created_at.desc())
        .limit(50)
    )

    purchases = result.scalars().all()

    return [
        {
            "id": p.id,
            "supplier_id": p.supplier_id,
            "total_cost": p.total_cost,
            "created_at": p.created_at
        }
        for p in purchases
    ]


# 🔥 5. DISPATCH LIST (UI READY)
@router.get("/dispatches")
async def get_dispatches(db: AsyncSession = Depends(get_db)):
    """Get all dispatches"""
    result = await db.execute(
        select(models.Dispatch)
        .order_by(models.Dispatch.created_at.desc())
        .limit(50)
    )

    dispatches = result.scalars().all()

    return [
        {
            "id": d.id,
            "customer_name": d.customer_name,
            "purpose": d.purpose,
            "created_at": d.created_at
        }
        for d in dispatches
    ]


# 🔥 6. ITEM LIST (WITH STOCK STATUS) - ANALYTICS VERSION
@router.get("/items/analytics/summary")
async def get_items_analytics_summary(db: AsyncSession = Depends(get_db)):
    """Get analytics summary for items page"""
    # Get total items count
    total_items = await db.scalar(select(func.count(models.Item.id)))
    
    # Get low stock count (items with quantity < 10 and > 0)
    low_stock_result = await db.execute(
        select(func.count(models.Item.id))
        .where(models.Item.quantity < 10)
        .where(models.Item.quantity > 0)
    )
    low_stock_count = low_stock_result.scalar() or 0
    
    # Get total quantity
    total_quantity_result = await db.scalar(select(func.sum(models.Item.quantity)))
    total_quantity = total_quantity_result or 0
    
    # Get total value (quantity * price for all items)
    result = await db.execute(select(models.Item))
    items = result.scalars().all()
    total_value = sum((item.quantity or 0) * (item.price or 0) for item in items)
    
    return {
        "total_items": total_items or 0,
        "low_stock_count": low_stock_count,
        "total_quantity": total_quantity,
        "total_value": total_value
    }


@router.get("/items/analytics/summary/list")
async def get_items_analytics(db: AsyncSession = Depends(get_db)):
    """Get all items with stock status for analytics"""
    result = await db.execute(select(models.Item))
    items = result.scalars().all()

    return [
        {
            "id": i.id,
            "name": i.name,
            "sku": i.sku,
            "price": i.price,
            "quantity": i.quantity,
            "stock_status": (
                "LOW" if i.quantity < 10 else "OK"
            )
        }
        for i in items
    ]
