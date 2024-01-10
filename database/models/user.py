from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.config.datebase import Base

class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(50), nullable=False)
	surname = Column(String(50), nullable=False)
	patronymic = Column(String(50))
	login = Column(String, nullable=False)
	password = Column(String(128), nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	role = Column(String(50), default="user", nullable=False)

__all__ = ['Users']