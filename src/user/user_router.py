from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import get_id_from_token, oauth2_scheme
from src.database import get_async_session
from src.main import SessionDep
from src.user.user_model import User
from src.user.user_role import UserRole
from src.user.user_schemas import UserCreate, UserOut, UserAuth, UserUpdate, UserCreateOut
from src.user.user_service import UserService
from src.utils.sms_service import send_verification_sms, confirm_sms_code

router = APIRouter(tags=["User"])


@router.post("/user", status_code=200, response_model=UserCreateOut)
async def create_user(user: UserCreate, session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user_db = User(**user.dict())
    user_db.role = UserRole.PATIENT
    return await user_service.create(user_db)


@router.post("/auth", status_code=200, response_model=UserCreateOut)
async def auth(user_auth: UserAuth, session: AsyncSession = SessionDep):
    user_service = UserService(session)
    return await user_service.auth(user_auth)


@router.get("/send_confirm_sms", status_code=200)
async def send_sms(number: int, session: AsyncSession = SessionDep):
    await send_verification_sms(number, session)
    return "Ok"


@router.get("/confirm_code", status_code=200)
async def send_sms(number: int, code: int, session: AsyncSession = SessionDep):
    await confirm_sms_code(number, code, session)
    return "Ok"


@router.get("/user")
async def get_user(user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)

    return UserOut(**(await user_service.get_user_by_id(user_id)).__dict__)


@router.get("/refresh")
async def refresh(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user = await user_service.refresh_tokens(token)
    access = user.access_token
    refresh = user.refresh_token

    return {
        "access_token": access.token,
        "refresh_token": refresh.token
    }


@router.put("/user", response_model=UserOut)
async def update_user(user_update: UserUpdate, user_id=2,
                      session: AsyncSession = SessionDep):
    user_service = UserService(session)
    return UserOut(**user_service.update_user(user_id, user_update).__dict__)
