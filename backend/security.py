import bcrypt

def hash_password(raw_password: str) -> str: # creates a secure hash for storing in the DB
    """Hash a plaintext password."""
    return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(raw_password: str, hashed_password: str) -> bool: # checks login attempts
    """Check if a raw password matches the stored hash."""
    if not hashed_password:
        return False
    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed_password.encode("utf-8"))
