from sqlalchemy.orm import Session
from .user_model import User
from .user_schemas import UserCreate, UserResponse
from fastapi import HTTPException
from app.classes.user_logger import UserLogger

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = UserLogger()

    def get_all(self):
        return self.db.query(User).all()

    def login(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email, User.password == password).first()
        if user:
            self.logger.user_login(user_id=user.user_id)
            return user
        else:
            self.logger.user_login_failed(email)
            raise HTTPException(status_code=401, detail="Invalid email or password")