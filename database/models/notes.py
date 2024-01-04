
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.config.datebase import Base

class Note(Base):
	__tablename__ = 'notes'
	id = Column(Integer, primary_key=True, autoincrement=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	
__all__ = ['Note']