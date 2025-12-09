from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
import datetime

# This creates a "base class" that all our models will inherit from
Base = declarative_base()

class User(Base):
    __tablename__ = "users"  # name of the table in the database

    id = Column(Integer, primary_key=True)        # unique ID for each user
    name = Column(String, nullable=False)         # user’s name
    email = Column(String, unique=True, nullable=False)  # must be unique
    phone = Column(String)                        # optional phone number
    role = Column(String, default="patron")       # "patron" or "staff"
    password_hash = Column(String)
    # One user can have many loans
    loans = relationship("Loan", back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)     # name of the item
    category = Column(String)                  # e.g., "Book", "Laptop"
    quantity = Column(Integer, default=1)      # how many copies available
    status = Column(String, default="available")  # available, checked_out, etc.

    # One item can have many loans
    loans = relationship("Loan", back_populates="item")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    checkout_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="loans")
    item = relationship("Item", back_populates="loans")
    fine = relationship("Fine", back_populates="loan", uselist=False)


class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))   # link to a Loan
    amount = Column(Float, default=0.0)                 # fine amount
    paid_status = Column(String, default="unpaid")      # unpaid / paid

    loan = relationship("Loan", back_populates="fine")


