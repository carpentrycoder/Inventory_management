# app/models.py
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from sqlalchemy.sql import func


# 🔹 1. Category
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)

    items = relationship("Item", back_populates="category")


# 🔹 2. Supplier
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_person = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    contact_info = Column(String, nullable=True)
    address = Column(Text, nullable=True)

    items = relationship("Item", back_populates="supplier")


# 🔹 3. Item
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    sku = Column(String, unique=True, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="items")
    supplier = relationship("Supplier", back_populates="items")
    stock_transactions = relationship("StockTransaction", back_populates="item")


# 🔹 4. User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="viewer")  # admin or viewer

    stock_transactions = relationship("StockTransaction", back_populates="user")


# 🔹 5. StockTransaction
class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    change_type = Column(String, nullable=False)  # IN / OUT
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=True)
    dispatch_id = Column(Integer, ForeignKey("dispatches.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    item = relationship("Item", back_populates="stock_transactions")
    user = relationship("User", back_populates="stock_transactions")
    purchase = relationship("Purchase", back_populates="stock_transactions")
    dispatch = relationship("Dispatch", back_populates="stock_transactions")

# 🔹 6. Purchase
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    total_cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    supplier = relationship("Supplier")
    stock_transactions = relationship("StockTransaction", back_populates="purchase")

# 🔹 7. Dispatch
class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    purpose = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    stock_transactions = relationship("StockTransaction", back_populates="dispatch")

# 🔹 5.AuditLog
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action = Column(String, nullable=False)          # CREATE / UPDATE / DELETE
    entity = Column(String, nullable=False)          # category / supplier / item
    entity_id = Column(Integer, nullable=False)

    description = Column(JSON, nullable=True)        # ✅ JSON field
    timestamp = Column(DateTime(timezone=True), server_default=func.now())