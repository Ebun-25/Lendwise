from .database import SessionLocal
from .models import User, Item, Loan, Fine
import datetime


def add_user(name, email, phone, role="patron"):
    session = SessionLocal()
    existing = session.query(User).filter_by(email=email).first()
    if existing:
        session.close()
        return existing  # don't crash
    user = User(name=name, email=email, phone=phone, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user

def add_item(title, category, quantity=1):
    session = SessionLocal()
    item = Item(title=title, category=category, quantity=quantity)
    session.add(item)
    session.commit()
    session.refresh(item)
    session.close()
    return item


def checkout_item(user_id, item_id, days=7):
    session = SessionLocal()
    item = session.get(Item, item_id)
    if item and item.quantity > 0:
        loan = Loan(
            user_id=user_id,
            item_id=item_id,
            due_date=datetime.datetime.utcnow() + datetime.timedelta(days=days)
        )
        item.quantity -= 1  # reduce stock
        session.add(loan)
        session.commit()
        session.refresh(loan)
        session.close()
        return loan
    else:
        session.close()
        return None

def return_item(loan_id, return_date=None):
    """Mark a loan as returned and create a fine if overdue."""
    session = SessionLocal()
    try:
        loan = session.query(Loan).filter_by(id=loan_id).first()
        if not loan:
            session.close()
            return None

        # Use provided date or now
        loan.return_date = return_date or datetime.datetime.now()
        session.add(loan)
        session.commit()

        # Check overdue and create fine
        if loan.return_date > loan.due_date:
            days_late = (loan.return_date - loan.due_date).days
            fine_amount = days_late * 1.0  # $1 per day late
            fine = Fine(loan_id=loan.id, amount=fine_amount, paid_status="unpaid")
            session.add(fine)
            session.commit()
            session.refresh(fine)
            session.close()
            return fine
        else:
            session.close()
            return None
    except:
        session.rollback()
        session.close()
        raise


def calculate_fine(loan_id, fine_per_day=1.0):
    session = SessionLocal()
    loan = session.get(Loan, loan_id)
    fine_record = None
    if loan and loan.return_date and loan.return_date > loan.due_date:
        days_overdue = (loan.return_date - loan.due_date).days
        fine_amount = days_overdue * fine_per_day
        fine_record = Fine(loan_id=loan.id, amount=fine_amount)
        session.add(fine_record)
        session.commit()
        session.refresh(fine_record)
    session.close()
    return fine_record
