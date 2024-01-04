from enum import Enum


class RegistrationStatus(Enum):
    # Коды для регистрации
	REGISTRATION_SUCCESS = "code_10_00"  				# Регистрация успешна
	USER_ALREADY_EXISTS = "code_10_01"   				# Пользователь уже существует
	INVALID_EMAIL_FORMAT = "code_10_02"  				# Недопустимый формат электронной почты
	WEAK_PASSWORD = "code_10_03"         				# Пароль не соответствует требованиям безопасности
	MISSING_FIELDS = "code_10_04"        				# Не заполнены обязательные поля
	EMAIL_VERIFICATION_ERROR = "code_10_05" 			# Ошибка подтверждения электронной почты
	UNEXPECTED_ERROR_REGISTRATION = "code_10_06" 		# Непредвиденная ошибка при регистрации.

class AuthorizationStatus(Enum):
	# Коды для авторизации
	AUTH_SUCCESS = "code_20_00"          				# Авторизация успешна
	INVALID_LOGIN = "code_20_01"         				# Неверный логин или пароль
	ACCOUNT_NOT_ACTIVATED = "code_20_02" 				# Аккаунт не активирован
	ACCOUNT_BLOCKED = "code_20_03"       				# Аккаунт заблокирован
	TWO_FACTOR_REQUIRED = "code_20_04"   				# Требуется двухфакторная аутентификация
	SESSION_EXPIRED = "code_20_05"       				# Сессия истекла
	UNEXPECTED_ERROR_AUTHENTICATION = "code_20_06" 		# Непредвиденная ошибка при авторизации.

class LogoutStatus(Enum):
	# Коды статуса для операции выхода из системы (logout)
	LOGOUT_SUCCESS = "code_30_00"          				# Выход из системы успешно выполнен
	NO_ACTIVE_SESSION = "code_30_01"       				# Не найдена активная сессия для завершения
	SESSION_TERMINATION_FAILED = "code_30_02" 			# Ошибка при попытке завершить сессию
	UNAUTHORIZED_ACCESS = "code_30_03"     				# Попытка выхода без авторизации
	UNEXPECTED_ERROR_LOGOUT = "code_30_04" 				# Непредвиденная ошибка при попытке выхода из системы

class AccessRights(Enum):
    ACCESS_DENIED = "code_40_00"  						# Доступ запрещен
    ADMIN_ACCESS = "code_40_01"   						# Доступ администратора
    USER_ACCESS = "code_40_02"    						# Доступ пользователя
    GUEST_ACCESS = "code_40_03"   						# Доступ гостя
    EDITOR_ACCESS = "code_40_04"  						# Доступ редактора
    MODERATOR_ACCESS = "code_40_05"  					# Доступ модератора
    READ_ONLY_ACCESS = "code_40_06"  					# Доступ только для чтения
    FULL_ACCESS = "code_40_07"    						# Полный доступ
    NO_ACCESS = "code_40_08"      						# Нет доступа
    LIMITED_ACCESS = "code_40_09" 						# Ограниченный доступ

class JWTStatus(Enum):
    JWT_CREATED = "code_50_00"         					# JWT успешно создан
    JWT_EXPIRED = "code_50_01"         					# JWT истек
    JWT_INVALID = "code_50_02"         					# Недействительный JWT
    JWT_VALID = "code_50_03"           					# JWT действителен
    JWT_REFRESH_REQUIRED = "code_50_04"  				# Требуется обновление JWT
    JWT_SIGNATURE_FAILED = "code_50_05"  				# Ошибка подписи JWT
    JWT_MISSING = "code_50_06"         					# JWT отсутствует
    JWT_DECODE_ERROR = "code_50_07"    					# Ошибка декодирования JWT
    JWT_INVALID_AUDIENCE = "code_50_08"					# Недействительная аудитория JWT
    JWT_INVALID_ISSUER = "code_50_09"  					# Недействительный издатель JWT
    JWT_ACCESS_DENIED = "code_50_10"   					# Доступ запрещен на основе JWT