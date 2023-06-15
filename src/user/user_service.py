from typing import Annotated

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.auth import get_password_hash, verify_password, create_access_token, create_refresh_token, \
    get_id_from_token
from src.user.user_model import User, RefreshToken
from src.user.user_schemas import UserAuth, UserUpdate, UserOut
from src.config import Config

data = Config()


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User):
        await self.check_phone(user.phone_number)
        user.password = get_password_hash(user.password)
        self.session.add(user)
        # await self.session.commit()
        return await self.create_tokens(user)

    async def get_user_by_phone(self, phone: int):
        stmt = select(User).filter_by(phone_number=phone)
        user = await self.session.scalar(stmt)
        return user

    async def get_user_by_id(self, user_id: int):
        stmt = select(User).filter_by(id=user_id)
        user = await self.session.scalar(stmt)
        if not user:
            raise HTTPException(status_code=400,
                                detail={"User not found"})
        return user

    async def check_phone(self, phone: int):
        if await self.get_user_by_phone(phone):
            raise HTTPException(status_code=400,
                                detail={"phone": f"User with phone number +{phone} already exist!"})

    async def auth(self, user_auth: UserAuth):
        user_db: User = await self.get_user_by_phone(user_auth.phone)
        if not user_db or not verify_password(user_auth.password, user_db.password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        return await self.create_tokens(user_db)

    async def create_tokens(self, user_db: User) -> UserOut:
        refresh_token = create_refresh_token(user_db)
        token = RefreshToken(token=refresh_token.token)
        token.exp = refresh_token.exp
        token.user = user_db
        self.session.add(token)
        await self.session.commit()
        user = UserOut(access_token=create_access_token(user_db), refresh_token=refresh_token, **user_db.__dict__)
        user.access_token = create_access_token(user_db)
        user.refresh_token = refresh_token
        return user

    async def refresh_tokens(self, token):
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        refresh_token_db: RefreshToken = await self.session.scalar(stmt)
        if not refresh_token_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        await self.session.delete(refresh_token_db)
        return await self.create_tokens(refresh_token_db.user)

    async def get_user_from_token(self, user_id: Annotated[int, Depends(get_id_from_token)]):
        return self.get_user_by_id(user_id)

    async def update_user(self, user_id: int, user_update: UserUpdate):
        user_db: User = await self.get_user_by_id(user_id)
        for field, value in user_update.dict().items():
            if value:
                setattr(user_db, field, value)
        await self.session.commit()
        return user_db

