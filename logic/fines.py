from backend.database import SessionLocal
from backend.models import Fine


def list_fines():
    session = SessionLocal()
    try:
        fines = session.query(Fine).all()
        if not fines:
            return ["✅ No fines found."]
        return [f"Loan {f.loan_id} → Fine: ${f.amount:.2f} ({f.paid_status})" for f in fines]
    except Exception as e:
        return [f"Error fetching fines: {e}"]
    finally:
        session.close()
