from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

import enum

class FileType(enum.Enum):
    MEDIA = "MEDIA"
    DOCUMENT = "DOCUMENT"
    REPORT = "REPORT"

class File(Base):
    __tablename__ = "files"
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    type = Column(Enum(FileType), nullable=False)
    checksum = Column(String(8), nullable=False)   
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, onupdate=func.now())
    url = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    hash = Column(Text, nullable=False)

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    author = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, onupdate=func.now())

