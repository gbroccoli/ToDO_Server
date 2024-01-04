import logging
from jose import jwt, JWTError
from datetime import datetime, timedelta
from envdatareader import EnvDataReader
from core.routers.code_status import JWTStatus

logger = logging.getLogger(__name__)

class Token:

	@classmethod
	def create_access_token(cls, data: dict):
		to_encode = data.copy()
		expire = datetime.now() + timedelta(hours=2)
		to_encode.update({"exp": expire.timestamp()})
		encoded_jwt = jwt.encode(to_encode, EnvDataReader().get_value("APP_KEY"), algorithm=EnvDataReader().get_value("APP_ALGORITHM"))
		return encoded_jwt

	@classmethod
	def create_refresh_token(cls, data: dict, remember: bool):
		to_encode = data.copy()
		expire = datetime.now() + (timedelta(days=30) if remember else timedelta(days=2))
		to_encode.update({"exp": expire.timestamp()})
		encoded_jwt = jwt.encode(to_encode, EnvDataReader().get_value("APP_KEY"), algorithm=EnvDataReader().get_value("APP_ALGORITHM"))
		return encoded_jwt

	@staticmethod
	def verify_token(token: str):
		try:
			# Декодирование токена
			payload = jwt.decode(token, EnvDataReader().get_value("APP_KEY"), algorithms=EnvDataReader().get_value("APP_ALGORITHM"))

			# Проверка срока действия
			exp = payload.get("exp")
			if exp and datetime.fromtimestamp(exp) < datetime.now():
				return False, "Token has expired"

			return {
				"code": JWTStatus.JWT_VALID,
				"type": "valid",
				"msg": "Token is valid"
			}
		except JWTError as e:
			print(str(e))
			return False, "Invalid token"
	
	@classmethod
	def decode_token(cls, token: str):
		try:
			decoded_token = jwt.decode(token, EnvDataReader().get_value("APP_KEY"), algorithms=[EnvDataReader().get_value("APP_ALGORITHM")])
			return decoded_token if decoded_token["exp"] >= datetime.now().timestamp() else None
		except JWTError:
			return None
	
	@classmethod
	def refresh_access_token(cls, refresh_token: str) -> str:
		decoded_token = cls.decode_token(refresh_token)
		if decoded_token is None:
			return JWTStatus.JWT_EXPIRED

		# Проверка дополнительных условий для refresh_token (например, не был ли он отозван)
		# ...

		user_data = {"id": decoded_token["id"], "login": decoded_token["login"]}  # Пример, зависит от вашей структуры данных
		return cls.create_access_token(user_data)