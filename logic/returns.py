from backend.database import SessionLocal
from backend.models import Loan, Item, Fine
import datetime

def return_item(item_id: int):
    session = SessionLocal()

    try:
        loan = (
            session.query(Loan)
            .filter(Loan.item_id == item_id, Loan.return_date == None)
            .first()
        )

        if not loan:
            return f"⚠️ No active loan found for item ID {item_id}."

        # Mark as returned
        loan.return_date = datetime.datetime.utcnow()

        # Restore item quantity
        item = loan.item
        item.quantity += 1
        item.status = "available"

        # Check overdue
        if loan.return_date > loan.due_date:
            days_late = (loan.return_date - loan.due_date).days
            fine_amount = days_late * 1.0  # $1 per day late
            fine = Fine(loan_id=loan.id, amount=fine_amount, paid_status="unpaid")
            session.add(fine)
            message = (
                f"✅ '{item.title}' returned. "
                f"⚠️ Overdue by {days_late} days. Fine: ${fine_amount:.2f}"
            )
        else:
            message = f"✅ '{item.title}' returned successfully."

        session.commit()
        return message

    except Exception as e:
        session.rollback()
        return f"Error: {str(e)}"

    finally:
        session.close()
