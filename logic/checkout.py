from datetime import datetime, timedelta
from backend.database import SessionLocal
from backend.models import Item, Loan


def checkout_item(user_id, item_id, loan_days=14):
    session = SessionLocal()
    try:
        item = session.get(Item, item_id)
        if not item:
            return f"❌ Item {item_id} not found."

        # Adjust for your field name; your model uses 'quantity', not 'stock'
        if item.quantity <= 0:
            return f"❌ Item '{item.title}' is out of stock."

        # reduce stock
        item.quantity -= 1
        due_date = datetime.now() + timedelta(days=loan_days)

        # create a loan record
        loan = Loan(
            user_id=user_id,
            item_id=item_id,
            checkout_date=datetime.now(),
            due_date=due_date,
            returned=False
        )
        session.add(loan)
        session.commit()

        return f"✅ Checked out '{item.title}', due on {due_date.date()}."
    except Exception as e:
        session.rollback()
        return f"Error: {e}"
    finally:
        session.close()
