from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    file = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
