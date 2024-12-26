from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    last_access = Column(DateTime)
