from backend.database import Base, engine
from backend.models import User, Item, Loan, Fine

print("📦 Creating lendwise.db and tables...")

# Create all tables defined in models.py
Base.metadata.create_all(bind=engine)

print("✅ Database and tables created successfully!")
