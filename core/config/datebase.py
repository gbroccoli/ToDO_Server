from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from typing import Dict
from envdatareader import EnvDataReader

class Base(DeclarativeBase):
    pass


envDB = EnvDataReader()

DB_CONFIG: Dict[str, str | int] = {
    "HOST": envDB.get_value("DB_HOST") or "",
    "PORT": int(envDB.get_value("DB_PORT", default=5432)),
    "USER": envDB.get_value("DB_USER"),
    "PASSWORD": envDB.get_value("DB_PASSWORD"),
    "NAME": str(envDB.get_value("DB_NAME")),
}

DATA_URL = f"postgresql+asyncpg://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{
    DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['NAME']}"

engine = create_async_engine(DATA_URL)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)
