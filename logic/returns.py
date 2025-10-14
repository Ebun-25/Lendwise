from datetime import datetime
from backend.database import SessionLocal
from backend.models import Item, Loan, Fine


def return_item(loan_id):
    session = SessionLocal()
    try:
        loan = session.get(Loan, loan_id)
        if not loan:
            return "❌ Loan not found."

        # mark as returned
        loan.return_date = datetime.now()

        # increase item quantity
        item = session.get(Item, loan.item_id)
        item.quantity += 1

        # calculate overdue fine if late
        if loan.return_date > loan.due_date:
            days_overdue = (loan.return_date - loan.due_date).days
            fine_amount = days_overdue * 0.50  # $0.50 per day
            fine = Fine(loan_id=loan.id, amount=fine_amount, paid_status="unpaid")
            session.add(fine)

        session.commit()
        return f"✅ Returned '{item.title}' successfully."
    except Exception as e:
        session.rollback()
        return f"Error: {e}"
    finally:
        session.close()
