from typing import Annotated

from fastapi import Depends

from src.models.user_model import User
from src.schemas.user_schemas import UserModel
from src.services.user_service import UserService
from src.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

user_service = Annotated[UserService, Depends(UserService)]
get_user = Annotated[UserModel, Depends(UserService(UnitOfWork()).get_user_from_token)]
