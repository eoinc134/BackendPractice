from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from .models import User, Habit, Completion
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os

# DATABASE CONFIGURATION #
sqlite_file_name = "habits.db"
load_dotenv()  # Load environment variables from .env file
sqlite_url = os.getenv("DATABASE_URL", f"sqlite:///{sqlite_file_name}")

connect_args = {"check_same_thread": False} if "sqlite" in sqlite_url else {}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

# FUNCTIONS #

# Create the database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
# Get a database session
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]

