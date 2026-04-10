# Inventory Management System

A FastAPI-based Inventory Management System with analytics dashboards, item/category/supplier CRUD, stock movement tracking, purchase/dispatch logging, and an interactive Jinja2-powered UI.

## Key Features

- Dashboard analytics with total items, stock, categories, and suppliers
- Item management with stock status and inventory valuation
- Category and supplier management pages
- Stock-in / stock-out transaction support
- Purchase and dispatch history APIs
- Reports page with charts, search, CSV export, and movement analytics
- User authentication with signup/login and password reset
- SQLite database persistence (`inventory.db`)

## Project Structure

- `app/main.py` - FastAPI application entry point
- `app/database.py` - Database connection and session setup
- `app/models.py` - SQLAlchemy ORM models for categories, suppliers, items, users, stock transactions, purchases, dispatches, and audit logs
- `app/schemas.py` - Pydantic request/response schemas
- `app/crud.py` - CRUD helpers for database operations
- `app/routers/inventory.py` - Inventory API endpoints
- `app/routers/users.py` - User-related API routes
- `app/auth/routes_auth.py` - Authentication endpoints
- `app/ui_router.py` - Server-side routes for frontend templates
- `app/templates/` - Jinja2 HTML templates for UI pages
- `requirements.txt` - Python dependencies
- `inventory.db` - SQLite database file
- `create_tables.py` - Helper for manually creating database tables
- `seed_data.py` - Seed script for sample data

## Requirements

The project uses the following main dependencies:

- `fastapi`
- `uvicorn`
- `SQLAlchemy`
- `sqlmodel`
- `pydantic`
- `jinja2`
- `python-jose`
- `passlib`
- `streamlit`

Full dependency list is available in `requirements.txt`.

## Installation

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload --port 8000
```

Then open the UI at:

- `http://127.0.0.1:8000/ui/dashboard`
- `http://127.0.0.1:8000/ui/items`
- `http://127.0.0.1:8000/ui/categories`
- `http://127.0.0.1:8000/ui/suppliers`
- `http://127.0.0.1:8000/ui/reports`

## API Endpoints

### Authentication

- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Log in and receive a bearer token
- `POST /auth/forgot-password` - Reset password for an existing user

### Categories

- `POST /inventory/categories/` - Create category
- `GET /inventory/categories/` - List categories
- `GET /inventory/categories/{category_id}` - Get a category
- `PUT /inventory/categories/{category_id}` - Update a category

### Suppliers

- `POST /inventory/suppliers/` - Create supplier
- `GET /inventory/suppliers/` - List suppliers
- `GET /inventory/suppliers/{supplier_id}` - Get a supplier
- `PUT /inventory/suppliers/{supplier_id}` - Update a supplier

### Items

- `POST /inventory/items/` - Create item
- `GET /inventory/items/` - List items
- `GET /inventory/items/{item_id}` - Get item
- `PUT /inventory/items/{item_id}` - Update item
- `DELETE /inventory/items/{item_id}` - Delete item
- `GET /inventory/items/{item_id}/ledger` - Get item stock ledger

### Stock Movement

- `POST /inventory/stock-in` - Add stock to an item
- `POST /inventory/stock-out` - Remove stock from an item
- `GET /inventory/stock-movements` - Get latest stock transactions

### Purchases & Dispatches

- `GET /inventory/purchases` - List purchase records
- `GET /inventory/dispatches` - List dispatch records

### Analytics

- `GET /inventory/dashboard/summary` - Inventory overview metrics
- `GET /inventory/items/analytics/summary` - Item analytics summary
- `GET /inventory/items/analytics/summary/list` - Item analytics list

## UI Pages

The front-end UI is served from Jinja2 templates in `app/templates` and rendered via `app/ui_router.py`.

- `dashboard.html` - main analytics dashboard
- `items.html` - item management
- `categories.html` - category management and analytics
- `suppliers.html` - supplier analytics and details
- `reports.html` - reports dashboard with charts and CSV export
- `login.html` - authentication page

## Database

This project uses SQLite by default. The database file is `inventory.db`.

Tables are created automatically at application startup via `app/main.py`.

You can also create tables manually with:

```powershell
python create_tables.py
```

And populate sample data with:

```powershell
python seed_data.py
```

## Notes

- CORS is enabled for development (`allow_origins=['*']`). Update for production.
- Authentication is implemented with JWT tokens and password hashing.
- Charts in the reports page use `Chart.js` via the UI templates.
- The UI can be accessed through the `/ui` routes rather than the raw API.

## License

This repository does not include a specified license. Add a `LICENSE` file if you want to define one.
