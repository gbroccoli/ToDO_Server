from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)

class User(BaseModel):
    login: str
    password: str
    remember: Optional[bool] = False


@app.post("/login")
async def main(user: User):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "ok"})

routers = [app] 