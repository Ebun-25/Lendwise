from backend.database import SessionLocal
from backend.models import User, Item

def list_users_and_items():
    session = SessionLocal()

    print("=== USERS (Patrons & Librarians) ===")
    users = session.query(User).all()
    for u in users:
        print(f"ID: {u.id} | Name: {u.name} | Email: {u.email} | Role: {u.role}")

    print("\n=== ITEMS ===")
    items = session.query(Item).all()
    for i in items:
        print(f"ID: {i.id} | Title: {i.title} | Category: {i.category} | Quantity: {i.quantity}")

    session.close()

if __name__ == "__main__":
    list_users_and_items()
