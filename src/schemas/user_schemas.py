import datetime

from pydantic import BaseModel, ConfigDict

from src.models.user_role import UserRole


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token: str
    exp: datetime.datetime


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    name: str
    surname: str
    patronymic: str
    photo: str | None = None
    phone_number: str


class UserCreate(UserBase):
    model_config = ConfigDict(from_attributes=True)
    password: str


class UserAuth(BaseModel):
    phone: str
    password: str


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    registered_at: datetime.datetime
    role: UserRole
    id: int


class UserModel(UserOut):
    id: int
    password: str


class UserCreateOut(UserOut):
    access_token: Token
    refresh_token: Token


class UserUpdate(BaseModel):
    name: str = None
    surname: str = None
    patronymic: str = None
    phone_number: str = None
