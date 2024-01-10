
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from core.config.datebase import Base

class Notes(Base):
	__tablename__ = 'notes'
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	title = Column(String(128), nullable=False)
	description = Column(Text, nullable=False)
	staus = Column(String(255), nullable=False, default="")
	due_date = Column(DateTime, nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	
__all__ = ['Notes']