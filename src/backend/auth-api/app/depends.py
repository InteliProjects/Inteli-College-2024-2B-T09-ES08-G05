from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.connection import Session
from app.db.models import UserModel
from decouple import config
from jose import jwt, JWTError
from app.auth_user import UserUseCases

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

def token_verifier(
        db_Session: Session = Depends(get_db_session),
        token = Depends(oauth_scheme)
):
    uc = UserUseCases(db_session=db_Session)
    uc.verify_token(access_token=token)

def get_current_user(
        db_session: Session = Depends(get_db_session),
        token: str = Depends(oauth_scheme)
):
    uc = UserUseCases(db_session=db_session)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db_session.query(UserModel).filter_by(email=payload['sub']).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token or user not found'
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
