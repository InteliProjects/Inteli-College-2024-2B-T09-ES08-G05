from sqlalchemy.orm import Session
from .document_model import File
from fastapi import HTTPException
from app.utils.hashing import generate_sha256_hash_from_url
from app.utils.checksum import generate_crc32_checksum_from_url

class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def hash_file(self, file_id: int):
        # search for the file in the database
        file = self.db.query(File).filter_by(file_id=file_id).first()

        # generates the hash of the file
        try:
            if not file:
                raise HTTPException(status_code=404, detail="File not found.")
            hash_result = generate_sha256_hash_from_url(file.url)
            file.hash = hash_result
            self.db.commit()
            self.db.refresh(file)

            return file
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found.")

    def checksum_file(self, file_id: int):
        # search for the file in the database
        file = self.db.query(File).filter_by(file_id=file_id).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found.")

        # generates the checksum of the file
        try:
            checksum_result = generate_crc32_checksum_from_url(file.url)
            file.checksum = checksum_result
            self.db.commit()
            self.db.refresh(file)

            return file
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found.")