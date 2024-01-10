import logging
# from core.config.datebase import async_session_maker
from sqlalchemy import text
from core.config.datebase import async_session_maker
from typing import NamedTuple
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

def parse_record(record):
	username, id, user_id, title, description, status, due_date, created_at = record
	
	due_date = due_date.isoformat() if due_date else None
	created_at = created_at.isoformat() if created_at else None

	return {
		"username": username,
		"id":id,
		"title":title,
		"description":description,
		"status":status,
		"due_date":due_date,
		"created_at":created_at
	}

class DatabaseCRUD:

	@classmethod
	async def create_user(cls, data: dict):
		query = text("INSERT INTO users (surname, name, patronymic, login, password, role) VALUES (:surname, :name, :patronymic, :login, :password, :role)")

		try:
			async with async_session_maker() as session:
				result = await session.execute(
					query, 
					{
						"surname": data["surname"],
						"name": data["name"],
						"patronymic": data["patronymic"],
						"login": data["login"],
						"password": data["password"],
						"role": data["role"],
					}
				)
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

		try:
			async with async_session_maker() as session:
				res = await session.execute(query, {'login': user})
				row = res.fetchall()

				if not row:
					return []

				return row
		except SQLAlchemyError as e:
			print("An error occurred: %s" % e)
	
	@classmethod
	async def login_user(cls, user: dict):
		query = text("select id, login, password, role from users where login = :login")

		try:
			async with async_session_maker() as session:
				res = await session.execute(query, {'login': user["login"]})
				row = res.fetchall()

				if not row:
					return
				
				return row[0]

		except SQLAlchemyError as e:
			print("An error occurred: %s" % e)
	
	@classmethod
	async def select_all_notes(cls, id: int):
		query = text('SELECT u.login, n.* FROM users u JOIN notes n ON u.id = n.user_id WHERE u.id = :id')

		try:
			async with async_session_maker() as session:
				res = await session.execute(query, {'id': id})
				notes = res.fetchall()

				if not notes:
					return []

				
				return [
					parse_record(note) for note in notes
				]

		except SQLAlchemyError as e:
			print(f"An error occurred: {e}")

	@classmethod
	async def select_one_note(cls, id: int):
		query = text("select * from notes where id = :id")

		try:
			async with async_session_maker() as session:
				result = await session.execute(query, {'id': id})
				row = result.fetchall()
				
				if not row:
					return "error"

				note_id, user_id, title, description, status, due_date, created_at = row[0]

				return {
					"id": id,
					"title": title,
					"description": description,
					"status": status,
					"due_date": due_date,
				}
				
		except SQLAlchemyError as e:
			print(f"An error occurred: {e}")
	
	@classmethod
	async def create_note(cls, note: object):
		
		due_date = note.get('due_date')

		query = text("INSERT INTO notes (user_id, title, description, staus, due_date) VALUES (:user_id, :title, :description, :status, :due_date)")

		data = {
				"user_id": note["user_id"],
				"title": note["title"],
				"description": note["description"],
				"status": note["status"],
				"due_date": due_date,
		}

		try:
			async with async_session_maker() as session:
				res = await session.execute(query, data)
				await session.commit()

				if res.rowcount > 0:
					return True
				else:
					False

		except SQLAlchemyError as e:
			print(f"An error occurred: {e}")

	@classmethod
	async def delete_notion(cls, id: int):
		query = text("DELETE FROM notes WHERE id = :id")

		try:
			async with async_session_maker() as session:
				res =  await session.execute(query,
								 {
									 "id": id
								 })
				
				await session.commit()
				
				return res
		except SQLAlchemyError as e:
			print(f"An error occurred: {e}")
