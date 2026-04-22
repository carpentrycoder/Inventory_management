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
- Database persistence (SQLite for development, PostgreSQL for production)

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

3. Configure environment variables:

```powershell
# Create .env file from template
Copy-Item .env.example .env

# Edit .env with your settings (required for production)
# Update SECRET_KEY with a strong random value
```

The `.env` file contains:
- `SECRET_KEY` - JWT secret (change in production!)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiry duration
- `DB_TYPE` - Database type (sqlite or postgres)
- `DB_NAME` - Database filename (for sqlite)
- `POSTGRES_DB` - PostgreSQL connection URL (for postgres)
- `API_HOST` - API server host
- `API_PORT` - API server port
- `API_BASE_URL` - API base URL
- `FRONTEND_BASE_URL` - Frontend URL



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

This project supports both SQLite (for development) and PostgreSQL (for production).

- For SQLite: Set `DB_TYPE=sqlite` and `DB_NAME=inventory.db`
- For PostgreSQL: Set `DB_TYPE=postgres` and `POSTGRES_DB=your_connection_url`

Tables are created via Alembic migrations. Run migrations with:

```bash
alembic upgrade head
```

You can also create tables manually with:

```powershell
python create_tables.py
```

And populate sample data with:

```powershell
python seed_data.py
```

## Authentication Features

The login page (`/ui/login`) provides three main features:

1. **Sign in** - Log in with your email and password
2. **Create account** - Register a new user account with email and password (min. 8 characters)
3. **Forgot password** - Reset your password by entering your email and new password

After successful login, your JWT token is stored in `localStorage` and used for subsequent API requests.

Password hashing uses Argon2 for secure storage. Tokens expire after the configured duration (default: 30 minutes).

## Deployment

### Using Docker

1. Build the Docker image:

```bash
docker build -t inventory-app .
```

2. Run the container:

```bash
docker run -p 8000:8000 --env-file .env inventory-app
```

### Using Docker Compose

For local development with PostgreSQL:

```bash
docker-compose up --build
```

### Production Deployment on Render

1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Create a new Web Service from Docker
4. Set environment variables in Render dashboard:
   - `SECRET_KEY`: A strong random key for JWT
   - `DB_TYPE`: postgres
   - `POSTGRES_DB`: Your Neon PostgreSQL connection string
   - `API_HOST`: 0.0.0.0
   - `API_PORT`: 8000
   - `FRONTEND_BASE_URL`: Your Render app URL
5. Deploy!

The app will automatically create database tables on first startup.

## Notes

- CORS is enabled for development (`allow_origins=['*']`). Update for production.
- Authentication is implemented with JWT tokens and password hashing (Argon2).
- Charts in the reports page use `Chart.js` via the UI templates.
- The UI can be accessed through the `/ui` routes rather than the raw API.
- Environment variables are loaded from `.env` file. See `.env.example` for configuration.

## License

This repository does not include a specified license. Add a `LICENSE` file if you want to define one.
