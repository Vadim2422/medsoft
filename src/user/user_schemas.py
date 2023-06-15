import datetime

from pydantic import BaseModel

from src.auth.auth import Token


class UserBase(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    name: str
    surname: str
    patronymic: str
    phone_number: int


class UserCreate(UserBase):
    password: str


class UserAuth(BaseModel):
    phone: int
    password: str


class UserOut(UserBase):
    registered_at: datetime.datetime
    access_token: Token
    refresh_token: Token
    id: int


class UserUpdate(BaseModel):
    name: str = None
    surname: str = None
    patronymic: str = None
    phone_number: int = None

