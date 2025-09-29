from sqlalchemy import create_engine #creates the connection to the database.
from sqlalchemy.orm import sessionmaker #makes “sessions” (temporary workspaces for talking to the DB).
from .models import Base #comes from models.py and is needed to create tables.

DATABASE_URL = "sqlite:///lendwise.db" #This tells SQLAlchemy which database to use.

engine = create_engine(DATABASE_URL, echo=True) #prints SQL statements to the terminal (great for learning/debugging)


SessionLocal = sessionmaker(bind=engine)#this creates session factory

def init_db():
    Base.metadata.create_all(engine)

