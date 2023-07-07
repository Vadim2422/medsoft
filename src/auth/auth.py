from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status
from src.config import *
from ..user.user_model import User
from ..user.user_role import UserRole

SECRET_KEY = secret_key
ALGORITHM = algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = refresh_token_expire_days


class Token(BaseModel):
    token: str
    exp: datetime


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(user: User, type_token: str, minutes=None, days=None):
    exp = datetime.utcnow()
    if minutes:
        exp += timedelta(minutes=minutes)
    else:
        exp += timedelta(days=days)
    to_encode = {"type": type_token,
                 "id": user.id,
                 "exp": exp}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, exp


def create_access_token(user: User, minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
    token, exp = create_token(user, "access", minutes=minutes)
    return Token(token=token, exp=exp)


def create_refresh_token(user: User):
    token, exp = create_token(user, "refresh", days=REFRESH_TOKEN_EXPIRE_MINUTES)
    return Token(token=token, exp=exp)


async def get_id_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        if id is None or payload.get("type") != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return id


def check_user_role(user: User, checked_role: str):
    if not user or user.role != checked_role:
        raise HTTPException(status_code=403)


def check_patient(user: User):
    check_user_role(user, "patient")


def check_doctor(user: User):
    check_user_role(user, "doctor")
