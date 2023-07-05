import datetime

from pydantic import BaseModel

from src.auth.auth import Token
from src.user.user_role import UserRole


class UserBase(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    name: str
    surname: str
    patronymic: str
    photo: int | None
    phone_number: int


class UserCreate(UserBase):
    password: str


class UserAuth(BaseModel):
    phone: int
    password: str


class UserOut(UserBase):
    registered_at: datetime.datetime
    role: UserRole
    id: int


class UserCreateOut(UserOut):
    access_token: Token
    refresh_token: Token


class UserUpdate(BaseModel):
    name: str = None
    surname: str = None
    patronymic: str = None
    phone_number: int = None
