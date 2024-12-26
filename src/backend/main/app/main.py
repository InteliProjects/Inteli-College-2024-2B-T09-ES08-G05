from fastapi import FastAPI
from app.modules.user.user_controller import UserController
from app.modules.document.document_controller import DocumentController
from app.database import Base, engine

app = FastAPI()

# Add routers 
app.include_router(UserController().get_router())
app.include_router(DocumentController().get_router())