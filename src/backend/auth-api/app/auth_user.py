from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import UserModel
from decouple import config
from app.schemas import User
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.classes.user_logger import UserLogger

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt']) 

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.logger = UserLogger()

    def user_register(self, user: User):
        user_model = UserModel(
            name = user.name,
            email = user.email,
            password = crypt_context.hash(user.password),
            created_at = datetime.utcnow(),
            last_access = datetime.utcnow(),
            role = user.role
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            self.logger.user_register(email=user_model.email)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='email already exists'
            )
        
    def user_login(self, user: User, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(email=user.email).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email or passsword' 
            )
        
        if not crypt_context.verify(user.password, user_on_db.password):
            self.logger.user_login_failed(user.email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email or password'
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': user.email,
            'exp': exp,
            'role': user.role
        }

        acess_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        self.logger.user_login(user_on_db.id)
        return {
            'access_token': acess_token,
            'exp': exp.isoformat()
        }
    
    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token' 
            )

        user_on_db = self.db_session.query(UserModel).filter_by(email=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
    
    def verify_admin(self, user: UserModel):
        if user.role != "Coordenador":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have coordenador privilegies"
            )