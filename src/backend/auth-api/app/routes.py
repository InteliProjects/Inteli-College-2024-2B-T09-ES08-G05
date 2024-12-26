from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm 
from app.depends import get_db_session, token_verifier, get_current_user
from app.db.models import UserModel
from app.auth_user import UserUseCases
from app.schemas import User

user_router = APIRouter(prefix='/user')
test_router = APIRouter(prefix='/test', dependencies=[Depends(token_verifier)])

@user_router.post('/register')
def user_register(
    user: User,
    db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )

@user_router.post('/login')
def user_register(
        request_form_user: OAuth2PasswordRequestForm = Depends(),
        db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session=db_session)

    user = User(
        email=request_form_user.username.strip(),
        password=request_form_user.password
    )

    auth_data = uc.user_login(user=user)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )

@test_router.post('/test')
def test_user_verify(token_verify = Depends(token_verifier)):
    return 'It works'

@test_router.post('/coordenador')
def coordenador_only(
    current_user: UserModel = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    
    uc = UserUseCases(db_session=db_session)
    uc.verify_admin(current_user)  
    return {"message": "Bem-vindo, coordenador!"}