from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth import auth
import schemas
from config import Config
from db import get_async_session, async_session_maker

from models.models import User

app = FastAPI(
    title="Trading App"
)
app.include_router(auth.router)

@app.post("/user")
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_session)):
    # db_user: User = User(firstname=user.firstname, secondname=user.secondname, patronymic=user.patronymic)
    db_user: User = User(**user.dict())
    db.add(db_user)
    await db.commit()
    # db.refresh(user)

    return user

@app.get("/user")
async def get_user(firstname: str, db: AsyncSession = Depends(get_async_session)):
    stmt = select(User).where(User.firstname == firstname)
    return await db.scalar(stmt)


@app.put("/user")
async def update_user(user_update: schemas.UserUpdate, db: AsyncSession = Depends(get_async_session)):
    # todo after added authenticate write with token and get user_id
    user_id = 8
    stmt = select(User).filter(User.id == user_id)
    user_db = await db.scalar(stmt)
    for field, value in user_update.dict().items():
        if value:
            setattr(user_db, field, value)
    await db.commit()
    return user_db