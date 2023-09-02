from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep, user_service, get_user
from src.models.user_role import UserRole
from src.services.doctor_service import DoctorService
from src.services.user_service import UserService
from src.auth.auth import oauth2_scheme, refresh_tokens
from src.models.user_model import User
from src.schemas.user_schemas import UserCreate, UserCreateOut, UserOut, UserAuth, UserModel
from src.utils.unitofwork import UnitOfWork

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("", status_code=201)
async def create_user(
        user: UserCreate,
        uow: UOWDep) -> UserCreateOut:
    return await UserService(uow).create_user(user)


@router.get("", status_code=200)
async def get_user(
        user: get_user
        ) -> UserOut:
    return UserOut.model_validate(user)


@router.post("/auth", status_code=200, response_model=UserCreateOut)
async def auth(user_auth: UserAuth,
               uow: UOWDep):
    return await UserService(uow).auth(user_auth)


@router.get("/refresh")
async def refresh_token(uow: UOWDep, token: Annotated[str, Depends(oauth2_scheme)]):
    access, refresh = await refresh_tokens(uow, token)

    return {
        "access_token": access.token,
        "refresh_token": refresh.token
    }
