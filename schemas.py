from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    firstname: str
    secondname: str
    patronymic: str


class UserUpdate(BaseModel):
    firstname: str = None
    secondname: str = None
    patronymic: str = None
