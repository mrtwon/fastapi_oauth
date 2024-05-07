from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import settings


class Session:
    pass


async def get_session() -> AsyncSession:
    async_engine = create_async_engine(
        url=settings.DATABASE_URL_asyncpg
    )
    session = async_sessionmaker(async_engine)
    async with session(expire_on_commit=False) as s:
        return s


def di_setup(app: FastAPI):
    app.dependency_overrides[Session] = get_session
