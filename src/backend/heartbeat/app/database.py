from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Create the connection engine
engine = create_engine(DATABASE_URL)

# Create the base for the models
Base = declarative_base()

# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
