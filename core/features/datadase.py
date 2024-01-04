import logging
# from core.config.datebase import async_session_maker
from sqlalchemy import text
from core.config.datebase import async_session_maker
from typing import NamedTuple
from sqlalchemy.exc import SQLAlchemyError

class DatabaseCRUD:

	@classmethod
	async def create_user(cls, data: dict):
		query = text("INSERT INTO users (surname, name, patronymic, login, password) VALUES (:surname, :name, :patronymic, :login, :password)")

		try:
			async with async_session_maker() as session:
				result = await session.execute(query, {"surname": data["surname"],"name": data["name"], "patronymic": data["patronymic"], "login": data["login"], "password": data["password"]})
				await session.commit()

				if result.rowcount > 0:
					return True
				else:
					return False
		except SQLAlchemyError as e:
			return False
	
	@classmethod
	async def select_user(cls, user: str):
		query = text("SELECT login FROM users WHERE login = :login")

		async with async_session_maker() as session:
			res = await session.execute(query, {'login': user})
			row = res.fetchall()
			return row
	
	@classmethod
	async def login_user(cls, user: dict):
		query = text("select id, login, password from users where login = :login")

		async with async_session_maker() as session:
			res = await session.execute(query, {'login': user["login"]})
			row = res.fetchall()
			return row
		
		

    # @classmethod
    # async def insertDB(cls, *, query: str, data: dict):
    #     logging.getLogger(__name__)
    #     try:
    #         async with async_session_maker() as session:
    #             querys = text(query)
    #             await session.execute(querys, data)
    #             await session.commit()

    #             return True
    #     except BaseException:
    #         return False

    # @classmethod
    # async def selectDB(cls, *, query: str, data: dict):
    #     logging.getLogger(__name__)
    #     try:
    #         async with async_session_maker() as session:
    #             querys = text(query)
    #             res = await session.execute(querys, data)
    #             rows = res.fetchall()
    #             return rows
    #     except SQLAlchemyError as e:
    #         return e

    # @classmethod
    # async def selectDB_one(cls, *, query: str, data: dict):
    #     logging.getLogger(__name__)
    #     try:
    #         async with async_session_maker() as session:
    #             querys = text(query)
    #             res = await session.execute(querys, data)
    #             rows = res.fetchone()
    #             return rows
    #     except SQLAlchemyError as e:
    #         return e
