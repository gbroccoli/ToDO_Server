from fastapi import Request, status
from fastapi.responses import JSONResponse
from core.features.jwt import Token
from core.routers.code_status import JWTStatus, AccessRights

response_false = JSONResponse(
		status_code=status.HTTP_403_FORBIDDEN,
		content={
			"code": AccessRights.ACCESS_DENIED.value,
			"type": "access",
			"msg": "Access denied"
		}
	)

def auth_user(request: Request):
    
	if request.cookies.get("access_token") != None:
		
		access_token = Token.verify_token(request.cookies.get("access_token"))

		if access_token["code"] == JWTStatus.JWT_VALID.value:
			return True

		return response_false
	
	return response_false
