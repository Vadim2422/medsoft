import random
from datetime import datetime, timedelta

import aiohttp
from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import *
from src.models.user_model import VerificationCode



async def get_code_by_phone(number, session):
    stmt = select(VerificationCode).where(and_(VerificationCode.phone_number == number))
    return await session.scalar(stmt)


async def send_sms(number: str, text: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://{sms_email}:{sms_key}@gate.smsaero.ru/v2/sms/send?number={number.replace('7', '')}&text={text}&sign=SMS Aero") as resp:
            if not (await resp.json()).get('success'):
                raise HTTPException(400)


async def send_verification_sms(number: str, session: AsyncSession):
    code = random.randint(10000, 99999)
    code_db = await get_code_by_phone(number, session)
    if not code_db:
        code_db = VerificationCode(phone_number=number, verification_code=code)
        session.add(code_db)
    else:
        code_db.verification_code = code
        code_db.created_at = datetime.now()

    await session.commit()
    text_msg = f"Код подтверждения - {code}"
    print(code)
    await send_sms(number, text_msg)


async def confirm_sms_code(number, code, session: AsyncSession):
    code_db: VerificationCode = await get_code_by_phone(number, session)
    if code_db and code_db.verification_code == code and (datetime.now() - code_db.created_at) <= timedelta(minutes=5):
        await session.delete(code_db)
        await session.commit()
    else:
        raise HTTPException(status_code=400, detail="Error")
