from backend.database import SessionLocal
from backend.models import Loan, Item, User
import datetime

def checkout_item(user_id: int, item_id: int):
    session = SessionLocal()

    try:
        user = session.query(User).filter_by(id=user_id).first()
        item = session.query(Item).filter_by(id=item_id).first()

        if not user:
            return "❌ Invalid Patron ID."

        if not item:
            return "❌ Invalid Item ID."

        if item.quantity <= 0:
            return f"⚠️ '{item.title}' is currently unavailable."

        # Create loan
        due_date = datetime.datetime.utcnow() + datetime.timedelta(days=14)
        loan = Loan(user_id=user.id, item_id=item.id, due_date=due_date)

        session.add(loan)
        item.quantity -= 1
        item.status = "checked_out"

        session.commit()
        return f"✅ '{item.title}' checked out to {user.name} (Due: {due_date.date()})"

    except Exception as e:
        session.rollback()
        return f"Error: {str(e)}"

    finally:
        session.close()
