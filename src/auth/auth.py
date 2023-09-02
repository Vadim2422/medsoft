from datetime import datetime, timedelta
from typing import Tuple

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status
from src.config import *
from ..repositories.token_repository import TokenRepository
from src.models.user_model import User, RefreshToken
from src.models.user_role import UserRole
from ..schemas.user_schemas import Token
from ..utils.unitofwork import IUnitOfWork

SECRET_KEY = secret_key
ALGORITHM = algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = refresh_token_expire_days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(str(password))


def get_type_payload(payload: dict):
    return payload.get('type')


def get_payload(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("id") is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


def decode_access_token(token: str) -> dict:

    payload = get_payload(token)
    if get_type_payload(payload) != "access":
        raise credentials_exception
    return payload


def decode_refresh_token(token: str) -> dict:
    payload = get_payload(token)
    if get_type_payload(payload) != "refresh":
        raise credentials_exception
    return payload


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
    return Token(token=token, exp=exp, user_id=user.id)


def create_refresh_token(user: User):
    token, exp = create_token(user, "refresh", days=REFRESH_TOKEN_EXPIRE_DAYS)
    return Token(token=token, exp=exp)


async def create_tokens(user_db: User) -> Tuple[Token, Token]:
    return create_access_token(user_db), create_refresh_token(user_db)


async def refresh_tokens(uow: IUnitOfWork, token):
    async with uow:
        refresh_token_db: RefreshToken = await uow.token.find_one(token=token)
        if not refresh_token_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials")

        await uow.token.delete(token=token)
        await uow.commit()
        user_id = decode_refresh_token(token).get('id')
        user = await uow.users.find_one(id=user_id)
    return await create_tokens(user)


def check_user_role(user: User, checked_role: UserRole):
    if not user or user.role != checked_role:
        raise HTTPException(status_code=403)


def check_patient(user: User):
    check_user_role(user, UserRole.PATIENT)


def check_doctor(user: User):
    check_user_role(user, "doctor")

# class PermissionsRouter:
#     def __init__(self, role: UserRole):
#         self.role = role
#
#     async def __call__(self, user_db: Annotated[User, Depends(UserService(UserRepository).get_user_from_token)]):
