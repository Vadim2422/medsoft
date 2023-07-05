import asyncio

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.doctor.doctor_model import Doctor
from src.user.user_model import User

l = sorted([3, 2, 1])
print(l)