from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from core.middleware.auth_user import auth_user
from core.features.datadase import DatabaseCRUD
from core.routers.code_status import AccessRights, CRUDStatus
from pydantic import BaseModel
from typing import Optional
from datetime import date
import json

class Note(BaseModel):
	title: str
	description: str
	user_id: int
	status: str
	due_date: Optional[date] = None

class EditNote(BaseModel):
	title: str
	description: str
	status: str
	due_date: Optional[date] = None


app = APIRouter(
	tags=['Notes'],
	prefix="/notes"
)

@app.get("/")
async def all_notion(id: int, request: Request):

	auth = auth_user(request)

	if auth != True:
		return auth

	res = await DatabaseCRUD.select_all_notes(id)
	
	return JSONResponse(status_code=status.HTTP_200_OK,
					 content={
						 "code": AccessRights.FULL_ACCESS.value,
						 "type": "access",
						 "msg": "Access",
						 "data": res
					 })

@app.post("/")
async def create_notion(note: Note, request: Request):

	auth = auth_user(request)

	if auth != True:
		return auth
	
	
	if not (note.title or note.status or note.description):
		return JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST,
			content={
				"code": CRUDStatus.MISSING_REQUIRED_FIELDS.value,
				"type": "note",
				"msg": "Не все обязательные поля заполнены"
			}
		)

	note_sample = {
		"user_id": int(note.user_id),
		"title": note.title,
		"description": note.description,
		"status": note.status,
		"due_date": note.due_date if note.due_date else None,
	}

	noteq = await DatabaseCRUD.create_note(note_sample)

	if noteq == False:
		return  JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST,
			content={
				"code": CRUDStatus.CREATE_FAILURE.value,
				"type": "note",
				"msg": "Произошла ошибка при создание!"
			}
		)
	
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content={
			"code": CRUDStatus.CREATE_SUCCESS.value,
			"type": "note",
			"msg": "Success creating note"
		}
	)

@app.get("/{id}")
async def edit(id: int, request: Request):
	auth = auth_user(request=request)

	if auth != True:
		return auth
	
	res = await DatabaseCRUD.select_one_note(id)

	if res == "error":
		return JSONResponse(
			status_code=status.HTTP_404_NOT_FOUND,
			content={
				"code": CRUDStatus.READ_FAILURE.value,
				"type": "error",
				"msg": "Not found notes",
			}
		)

	return {
		"code": CRUDStatus.READ_SUCCESS.value,
		"type": "edit",
		"msg": "Edit successfully",
		"data": res
	}

@app.patch("/{id}")
async def edit_notion(id: int, note: EditNote):
	pass

@app.delete("/{id}")
async def delete_note(id: int, request: Request):
	
	auth = auth_user(request=request)

	if auth != True:
		return auth
	
	res  = await DatabaseCRUD.delete_notion(id=id)

	if res.rowcount == 0:
		return JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST,
			content={
				"code": CRUDStatus.DELETE_FAILURE.value,
				"type": "note",
				"msg": "Delete failed"
			}
		)
	
	return JSONResponse(
			status_code=status.HTTP_200_OK,
			content={
				"code": CRUDStatus.DELETE_SUCCESS.value,
				"type": "note",
				"msg": "Delete successfully"
			}
		)

routers = [app]