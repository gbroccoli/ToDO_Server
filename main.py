from fastapi import FastAPI
import uvicorn
from envdatareader import EnvDataReader
from core.config.app import Config
import logging

app = FastAPI()
env = EnvDataReader()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Config().run(app=app)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)