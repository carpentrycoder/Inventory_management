"""
ui_router.py  —  Frontend UI routes with server-side rendering
Serves templates with data context and handles page rendering
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pathlib import Path
from . import database, models, crud

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

ui_router = APIRouter(prefix="/ui", tags=["UI"])


# ========================
# AUTH PAGES
# ========================

@ui_router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def ui_login(request: Request):
    """Login/Signup page"""
    return templates.TemplateResponse("login.html", {"request": request})


# ========================
# DASHBOARD
# ========================

@ui_router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def ui_dashboard(request: Request, db: AsyncSession = Depends(database.get_db)):
    """Dashboard with analytics"""
    # Get summary stats
    total_items = await db.scalar(select(func.count(models.Item.id))) or 0
    total_stock = await db.scalar(select(func.sum(models.Item.quantity))) or 0
    total_cats = await db.scalar(select(func.count(models.Category.id))) or 0
    total_sups = await db.scalar(select(func.count(models.Supplier.id))) or 0

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "active": "dashboard",
        "total_items": total_items,
        "total_stock": total_stock,
        "total_categories": total_cats,
        "total_suppliers": total_sups
    })


# ========================
# ITEMS
# ========================

@ui_router.get("/items", response_class=HTMLResponse, include_in_schema=False)
async def ui_items(request: Request, db: AsyncSession = Depends(database.get_db)):
    """Items management page"""
    return templates.TemplateResponse("items.html", {
        "request": request,
        "active": "items"
    })


# ========================
# CATEGORIES
# ========================

@ui_router.get("/categories", response_class=HTMLResponse, include_in_schema=False)
async def ui_categories(request: Request, db: AsyncSession = Depends(database.get_db)):
    """Categories management page"""
    return templates.TemplateResponse("categories.html", {
        "request": request,
        "active": "categories"
    })


# ========================
# SUPPLIERS
# ========================

@ui_router.get("/suppliers", response_class=HTMLResponse, include_in_schema=False)
async def ui_suppliers(request: Request, db: AsyncSession = Depends(database.get_db)):
    """Suppliers management page"""
    return templates.TemplateResponse("suppliers.html", {
        "request": request,
        "active": "suppliers"
    })


# ========================
# REPORTS
# ========================

@ui_router.get("/reports", response_class=HTMLResponse, include_in_schema=False)
async def ui_reports(request: Request, db: AsyncSession = Depends(database.get_db)):
    """Reports and analytics page"""
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "active": "reports"
    })


# ========================
# ROOT REDIRECT
# ========================

@ui_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def ui_root(request: Request):
    """Redirect to dashboard"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/ui/dashboard")
