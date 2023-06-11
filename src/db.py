from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.config import Config

data = Config()


class Base(AsyncAttrs, DeclarativeBase):
    pass


DATABASE_URL = f"postgresql+asyncpg://{data.p_user}:{data.p_password}@{data.p_host}:{data.p_port}/{data.p_name}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

