from pydantic import BaseModel, Field
from typing import Optional,Dict, Any
from datetime import datetime


# 🔹 Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# 🔹 Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    contact_info: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True


# 🔹 Item Schemas
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    quantity: int
    price: float
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    total_price: Optional[float] = None  # Calculated field, returned in response
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 🔹 StockTransaction Schemas
class StockTransactionBase(BaseModel):
    item_id: int
    change_type: str  # IN / OUT
    quantity: int
    user_id: Optional[int] = None
    purchase_id: Optional[int] = None
    dispatch_id: Optional[int] = None
    notes: Optional[str] = None

class StockTransactionCreate(StockTransactionBase):
    pass

class StockTransaction(StockTransactionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# ------------------------------------------------------

# 🔹 User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str  # plain password input

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

# -----------------------------------

# 🔐 JWT Auth Schemas
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class ForgotPassword(BaseModel):
    username: str
    new_password: str = Field(
        min_length=6,
        max_length=72,
        description="Password must be 6–72 characters"
    )

class AuditLog(BaseModel):
    id: int
    user_id: int
    action: str
    entity: str
    entity_id: int
    description: Optional[Dict[str, Any]]   # ✅ JSON dict
    timestamp: datetime

    class Config:
        from_attributes = True