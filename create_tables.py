
from app.database import engine
from app import models

# 👇 This will create all tables in the database
print("📦 Creating tables in PostgreSQL...")
models.Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully.")