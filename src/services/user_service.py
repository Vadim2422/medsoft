from typing import Annotated

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from starlette import status

from src.auth.auth import get_password_hash, create_tokens, oauth2_scheme, verify_password, decode_access_token
from src.models.user_model import User, RefreshToken
from src.models.user_role import UserRole
from src.schemas.user_schemas import UserCreate, UserCreateOut, UserAuth, UserModel
from src.services.base_service import BaseService
from src.utils.unitofwork import IUnitOfWork, UnitOfWork


class UserService(BaseService):

    async def get_user_by_phone(self, phone_number: str) -> User:
        async with self.uow:
            return await self.uow.users.find_one(phone_number=phone_number)

    async def get_user_by_id(self, user_id: int) -> UserModel:
        async with self.uow:
            return await self.uow.users.find_one(id=user_id)

    async def check_phone(self, phone_number: str) -> None:
        if await self.get_user_by_phone(phone_number):
            raise HTTPException(status_code=400,
                                detail={"phone": f"User with phone number {phone_number} already exist!"})

    async def create_user(self, user: UserCreate) -> UserCreateOut:
        await self.check_phone(user.phone_number)
        async with self.uow:
            user.password = get_password_hash(user.password)
            user_db: User = User(**user.model_dump())
            user_db.role = UserRole.PATIENT
            await self.uow.users.create(user_db)
            await self.uow.commit()
            access, refresh = await create_tokens(user_db)
            refresh_db: RefreshToken = RefreshToken(token=refresh.token, exp=refresh.exp, user=user_db)
            await self.uow.token.create(refresh_db)
        return UserCreateOut(**user_db.__dict__,
                             access_token=access,
                             refresh_token=refresh)

    async def auth(self, user_auth: UserAuth):
        user: User = await self.get_user_by_phone(user_auth.phone)
        if not user or not verify_password(user_auth.password, user.password):
            raise HTTPException(status_code=403, detail="Incorrect email or password")
        access, refresh = await create_tokens(user)
        refresh_db: RefreshToken = RefreshToken(token=refresh.token, exp=refresh.exp)
        async with self.uow:
            await self.uow.token.create(refresh_db)
            await self.uow.commit()
        return UserCreateOut(**user.__dict__,
                             access_token=access,
                             refresh_token=refresh)

    async def get_user_from_token(self, token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:

        payload = decode_access_token(token)
        return await self.get_user_by_id(payload.get('id'))

    @staticmethod
    async def check_user_role(user_db: User, checked_role: UserRole):
        if not user_db or user_db.role != checked_role:
            raise HTTPException(status_code=403)
        return user_db

    async def auth_patient(self, token: Annotated[str, Depends(oauth2_scheme)]):
        return await self.check_user_role(await self.get_user_from_token(token), UserRole.PATIENT)

    async def auth_doctor(self, token: Annotated[str, Depends(oauth2_scheme)]):
        return await self.check_user_role(await self.get_user_from_token(token), UserRole.DOCTOR)
