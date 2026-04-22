from fastapi import FastAPI
from . import models, database
from .routers import inventory, users, seed
from .auth import routes_auth  # 👈 import your auth router
from .ui_router import ui_router  # 👈 import UI router
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Inventory Management System",
    description="A FastAPI-based system to manage stock, suppliers, and categories",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include Routers
app.include_router(routes_auth.router)   # 👈 Add this
app.include_router(inventory.router)
app.include_router(users.router)         # 👈 Add this
app.include_router(seed.router)          # 👈 Seed data router
app.include_router(ui_router)            # 👈 Add this

# ✅ Async DB Table Creation
async def init_models():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# ✅ Startup event to create tables
@app.on_event("startup")
async def on_startup():
    await init_models()

# ✅ Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Inventory Management System API"}
