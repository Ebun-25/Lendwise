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

from .security import hash_password, verify_password
from .models import User
from .database import SessionLocal

def create_user(name, email, phone, role="patron", password="changeme"):
    """Add a new user with a hashed password."""
    session = SessionLocal()
    try:
        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role,
            password_hash=hash_password(password)
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        session.close()

def authenticate(email, password):#checks email and password when someone logs in
    """Validate user credentials."""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.password_hash):
            return user
        return None
    finally:
        session.close()

from sqlalchemy import or_

def search_items(keyword):
    """Search for items by title or category."""
    session = SessionLocal()
    try:
        results = session.query(Item).filter(
            or_(
                Item.title.ilike(f"%{keyword}%"),
                Item.category.ilike(f"%{keyword}%")
            )
        ).all()
        return results
    finally:
        session.close()

def generate_reports():
    """Return summaries of loans, returns, and fines."""
    session = SessionLocal()
    try:
        total_loans = session.query(Loan).count()
        returned_loans = session.query(Loan).filter(Loan.return_date.isnot(None)).count()
        unpaid_fines = session.query(Fine).filter(Fine.paid_status == "unpaid").count()

        report = {
            "Total Loans": total_loans,
            "Returned Loans": returned_loans,
            "Unpaid Fines": unpaid_fines
        }
        return report
    finally:
        session.close()
