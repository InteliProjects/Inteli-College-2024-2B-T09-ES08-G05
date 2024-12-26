from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .document_service import DocumentService
from app.database import get_db

class DocumentController:
    def __init__(self):
        self.router = APIRouter(prefix="/documents", tags=["documents"])
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/hash")
        def hash_file(file_id: int, db = Depends(get_db)):
            document_service = DocumentService(db)
            try:
                document = document_service.hash_file(file_id= file_id)
                return document
            except HTTPException as e:
                raise e
            
        @self.router.post("/checksum")
        def checksum_file(file_id: int, db = Depends(get_db)):
            document_service = DocumentService(db)
            try:
                document = document_service.checksum_file(file_id= file_id)
                return document
            except HTTPException as e:
                raise e

    def get_router(self) -> APIRouter:
        return self.router
