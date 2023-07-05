from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.config import *




class Base(AsyncAttrs, DeclarativeBase):
    pass


DATABASE_URL = f"postgresql+asyncpg://{p_user}:{p_password}@{p_host}:{p_port}/{p_name}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

