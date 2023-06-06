import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv("src/config/.env")

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", None)
ENVIRONMENT = os.environ.get("ENV", None)

db_logs = "debug" if ENVIRONMENT == "development" else True
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=db_logs)


async def get_db_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
