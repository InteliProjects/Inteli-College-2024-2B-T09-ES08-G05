from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .user_schemas import UserCreate, UserResponse, LoginRequest
from .user_service import UserService
from app.database import get_db
from sqlalchemy.orm import Session

class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="", tags=["users"])
        self.setup_routes()

    def setup_routes(self):
        # Listando usuários
        @self.router.post("/login")
        def login(login_data: LoginRequest, db = Depends(get_db)):
            user_service = UserService(db)
            try:
                user = user_service.login(email=login_data.email, password=login_data.password)
                return user
            except HTTPException as e:
                raise e
            
        @self.router.get("/heart")
        def heart():
            return True

    def get_router(self) -> APIRouter:
        return self.router
