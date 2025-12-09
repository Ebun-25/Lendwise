from backend.database import SessionLocal
from backend.models import Fine, Loan, User, Item

def list_fines():
    session = SessionLocal()
    fines_info = []

    try:
        fines = (
            session.query(Fine)
            .join(Loan, Fine.loan_id == Loan.id)
            .join(User, Loan.user_id == User.id)
            .join(Item, Loan.item_id == Item.id)
            .filter(Fine.paid_status == "unpaid")
            .all()
        )

        if not fines:
            return ["✅ No unpaid fines found."]

        for fine in fines:
            fines_info.append(
                f"💰 {fine.loan.user.name} - \"{fine.loan.item.title}\": ${fine.amount:.2f} ({fine.paid_status})"
            )

        return fines_info

    except Exception as e:
        session.rollback()
        return [f"Error retrieving fines: {str(e)}"]

    finally:
        session.close()
