# Reuse the backend database connection
from backend.database import SessionLocal, init_db

# Optional: make sure tables exist before using
init_db()

# Get a session when needed
def get_session():
    return SessionLocal()
