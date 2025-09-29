from backend.database import init_db
from backend.repository import add_user, add_item, checkout_item, return_item
import datetime

# Initialize DB
init_db()

# Add user
user = add_user("John Doe", "john@example.com", "123-456")
print("User:", user.id, user.name)

# Add item
item = add_item("Python Crash Course", "Book", 3)
print("Item:", item.id, item.title)

# Checkout
loan = checkout_item(user.id, item.id, 7)
print("Loan:", loan.id, "Due:", loan.due_date)

# -------------------------
# Case 1: On-time return
# -------------------------
on_time_date = loan.due_date
fine1 = return_item(loan.id, on_time_date)
print("On-time return fine:", fine1.amount if fine1 else "No fine")

# -------------------------
# Case 2: Late return (3 days late)
# -------------------------
# Checkout again for fresh loan
loan2 = checkout_item(user.id, item.id, 7)
print("Loan 2:", loan2.id, "Due:", loan2.due_date)

late_date = loan2.due_date + datetime.timedelta(days=3)
fine2 = return_item(loan2.id, late_date)
print("Late return fine:", fine2.amount if fine2 else "No fine")
