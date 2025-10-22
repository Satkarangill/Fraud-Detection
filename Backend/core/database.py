from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Creating a database url in project folder
import os
# Get the directory where this file is located
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'database.db')
DATABASE_URL = f"sqlite:///{db_path}"

# Connecting python to database
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# SessionLocal class to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Table models will inherit from this class
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

