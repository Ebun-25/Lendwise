from datetime import datetime
from backend.database import SessionLocal
from backend.models import Loan, Fine


def check_overdue():
    session = SessionLocal()
    try:
        # find loans that are past due and not yet returned
        overdue_loans = session.query(Loan).filter(
            Loan.return_date == None,
            Loan.due_date < datetime.now()
        ).all()

        count = 0
        for loan in overdue_loans:
            days_overdue = (datetime.now() - loan.due_date).days
            fine_amount = days_overdue * 0.50  # 50¢ per day

            # Check if a fine already exists for this loan
            existing_fine = session.query(Fine).filter_by(loan_id=loan.id).first()
            if not existing_fine:
                fine = Fine(
                    loan_id=loan.id,
                    amount=fine_amount,
                    paid_status="unpaid"
                )
                session.add(fine)
                count += 1

        session.commit()
        return f"✅ {count} overdue fines processed."
    except Exception as e:
        session.rollback()
        return f"Error checking overdue: {e}"
    finally:
        session.close()
