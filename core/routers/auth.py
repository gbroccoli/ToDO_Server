from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Literal
from core.features.password import check_password_strength
from .code_status import AuthorizationStatus, RegistrationStatus, LogoutStatus, JWTStatus
from core.features.datadase import DatabaseCRUD
from core.config.hashing import PasswordManager
from core.features.jwt import Token

app = APIRouter(
	tags=["Auth"],
	prefix="/auth"
)

class Code(BaseModel):
	code: str
	type: Literal['success', "error"]
	msg: str

class Nominee(BaseModel):
	name: str
	surname: str
	patronymic: Optional[str] = None
	login: str
	password: str

class User(BaseModel):
	login: str
	password: str
	remember: bool = False


@app.post("/login")
async def login(user: User, response: Response):
	if not (user.login and user.password):
		return JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST, content={
				"code": RegistrationStatus.MISSING_FIELDS,
				"type": "error",
				"msg": "Не заполнены обязательные поля"
			})
	
	user_res = await DatabaseCRUD.login_user({"login": user.login, "password": user.password})
	

	if not user_res:
		return JSONResponse(
			status_code=status.HTTP_401_UNAUTHORIZED,
			content={
				"code": AuthorizationStatus.INVALID_LOGIN,
				"type": "error",
				"msg": "Неверный логин или пароль"
			}
		)
	
	id, login, password = user_res[0]
	if not PasswordManager.verify_password(user.password, password):
		return JSONResponse(
			status_code=status.HTTP_401_UNAUTHORIZED,
			content={
				"code": AuthorizationStatus.INVALID_LOGIN,
				"type": "error",
				"msg": "Неверный логин или пароль"
			}
		)

	access_token = Token.create_access_token({"id": id, "login": user.login})
	refresh_token = Token.create_refresh_token({"id": id, "login": user.login}, user.remember)

	response.set_cookie(
		key="access_token",
		value=access_token,
		httponly=True,
		max_age=7200
	)

	response.set_cookie(
		key="refresh_token",
		value=refresh_token,
		httponly=True,
		max_age=30 * 24 * 60 * 60 if user.remember else 172800
	)

	return {
		"code": AuthorizationStatus.AUTH_SUCCESS,
		"type": "success",
		"msg": "success"
	}



@app.post("/register")
async def register(nominee: Nominee):
	if not (nominee.surname and nominee.name and nominee.login and nominee.password):
		return JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST, content={
				"code": RegistrationStatus.MISSING_FIELDS,
				"type": "error",
				"msg": "Не заполнены обязательные поля"
			})
	
	if not check_password_strength(nominee.password):
		return JSONResponse(status=status.HTTP_401_UNAUTHORIZED, content={
			"code": RegistrationStatus.WEAK_PASSWORD,
			"type": "error",
			"msg": "Пароль не соответвует требованиям"
		})

	incident = await DatabaseCRUD.select_user(nominee.login)

	if incident:
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
			"code": RegistrationStatus.USER_ALREADY_EXISTS,
			"type": "error",
			"msg": "Данный пользователь уже существует" 
		})
	
	user_incident = {
		"login": nominee.login,
		"password": PasswordManager.hash_password(nominee.password),
		"surname": nominee.surname,
		"name": nominee.name,
		"patronymic": nominee.patronymic
	}

	user = await DatabaseCRUD.create_user(user_incident)

	if not user:
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
			"code": RegistrationStatus.UNEXPECTED_ERROR_REGISTRATION,
			"type": "error",
			"msg": "Произошла непредвидинная ошибка!"
		})
	
	return JSONResponse(
		status_code=status.HTTP_201_CREATED, 
		content={
			"code": RegistrationStatus.REGISTRATION_SUCCESS,
			"type": "success",
			"mgs": "Регестрация прошла успешно!"
		})
	
@app.get("/authorization")
async def authorization(request: Request, response: Response):

	if request.cookies.get("access_token") == None:
		if request.cookies.get("refresh_token") != None:

			refresh_token = Token.verify_token(token=request.cookies.get("refresh_token"))

			if refresh_token["code"] == JWTStatus.JWT_VALID:
				access_token = Token.refresh_access_token(refresh_token=request.cookies.get("refresh_token"))

				response.set_cookie(
					key="access_token",
					value=access_token,
					max_age=7200,
					httponly=True
				)

				return {
						"code": JWTStatus.JWT_VALID,
						"type": "success",
						"msg": "Досуп разрешен"
					}
		return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
			"code": JWTStatus.JWT_ACCESS_DENIED.value,
			"type": "error",
			"msg": "Access denied"
			})

	access_token_veri = Token.verify_token(token=request.cookies.get("access_token"))

	if access_token_veri["code"] == JWTStatus.JWT_VALID:
		return {
			"code": JWTStatus.JWT_VALID,
			"type": "success",
			"msg": "Досуп разрешен"
		}

	return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
			"code": JWTStatus.JWT_ACCESS_DENIED.value,
			"type": "error",
			"msg": "Access denied"
			}) 

@app.post("/refresh")
async def refresh(response: Response):
	pass

@app.post("/logout", response_model=Code)
async def logout(response: Response, request: Request):
	if request.cookies:
		response.delete_cookie(
			key="access_token",
			httponly=True
		)

		response.delete_cookie(
			key="refresh_token",
			httponly=True
		)

		return {
			"code": LogoutStatus.LOGOUT_SUCCESS,
			"type": "success",
			"msg": "Вы успешно вышли из учётной записи!"
		}

	return {
		"code": LogoutStatus.UNAUTHORIZED_ACCESS,
		"type": "error",
		"msg": "Доступ запрещен"
	}


routers = [app]