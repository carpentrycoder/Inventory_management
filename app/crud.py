# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

# --------------------------------------
# CATEGORY CRUD OPERATIONS
# --------------------------------------
async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    return result.scalar_one_or_none()

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Category).offset(skip).limit(limit))
    return result.scalars().all()

# --------------------------------------
# SUPPLIER CRUD OPERATIONS
# --------------------------------------
async def create_supplier(db: AsyncSession, supplier: schemas.SupplierCreate):
    db_supplier = models.Supplier(**supplier.dict())
    db.add(db_supplier)
    await db.commit()
    await db.refresh(db_supplier)
    return db_supplier

async def get_supplier(db: AsyncSession, supplier_id: int):
    result = await db.execute(select(models.Supplier).filter(models.Supplier.id == supplier_id))
    return result.scalar_one_or_none()

async def get_suppliers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Supplier).offset(skip).limit(limit))
    return result.scalars().all()

# --------------------------------------
# ITEM CRUD OPERATIONS
# --------------------------------------
async def create_item(db: AsyncSession, item: schemas.ItemCreate):
    # Calculate total_price before creating the item
    total_price = item.quantity * item.price
    db_item = models.Item(**item.dict(), total_price=total_price)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    return result.scalar_one_or_none()

async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Item).offset(skip).limit(limit))
    return result.scalars().all()

async def update_item(db: AsyncSession, item_id: int, item_update: schemas.ItemCreate):
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        await db.commit()
        await db.refresh(db_item)
    return db_item

async def delete_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item:
        await db.delete(db_item)
        await db.commit()
    return db_item

# --------------------------------------
# USER CRUD OPERATIONS
# --------------------------------------
async def create_user(db: AsyncSession, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, hashed_password=hashed_password, role="viewer")
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalar_one_or_none()

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalar_one_or_none()

# --------------------------------------
# STOCK TRANSACTION CRUD OPERATIONS
# --------------------------------------
async def create_stock_transaction(db: AsyncSession, transaction: schemas.StockTransactionCreate):
    db_transaction = models.StockTransaction(**transaction.dict())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_stock_transaction(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(models.StockTransaction).filter(models.StockTransaction.id == transaction_id))
    return result.scalar_one_or_none()

async def get_stock_transactions_for_item(db: AsyncSession, item_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.StockTransaction)
        .filter(models.StockTransaction.item_id == item_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# --------------------------------------
# CATEGORY UPDATE CRUD
# --------------------------------------
async def update_category(
    db: AsyncSession,
    category_id: int,
    category_update: schemas.CategoryCreate
):
    result = await db.execute(
        select(models.Category).filter(models.Category.id == category_id)
    )
    db_category = result.scalar_one_or_none()

    if db_category:
        update_data = category_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)

        await db.commit()
        await db.refresh(db_category)

    return db_category

# --------------------------------------
# SUPPLIER UPDATE CRUD
# --------------------------------------
async def update_supplier(
    db: AsyncSession,
    supplier_id: int,
    supplier_update: schemas.SupplierCreate
):
    result = await db.execute(
        select(models.Supplier).filter(models.Supplier.id == supplier_id)
    )
    db_supplier = result.scalar_one_or_none()

    if db_supplier:
        update_data = supplier_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_supplier, key, value)

        await db.commit()
        await db.refresh(db_supplier)

    return db_supplier

# --------------------------------------
# AUDIT LOG CRUD (JSON)
# --------------------------------------
async def create_audit_log(
    db: AsyncSession,
    user_id: int,
    action: str,
    entity: str,
    entity_id: int,
    description: dict | None
):
    log = models.AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        description=description   # ✅ dict directly
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log