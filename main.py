import uvicorn
from fastapi import FastAPI
from envdatareader import EnvDataReader
from core.config.app import Config


env = EnvDataReader()

app = FastAPI()

Config().run(app=app)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)