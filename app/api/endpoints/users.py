from fastapi import APIRouter
from fastapi import Depends

from app.api.schemas import UserCreateParameters
from app.api.schemas import UserCreateResponse
from app.services import UserService
from app.utils import IUnitOfWork
from app.utils import UnitOfWork

router = APIRouter(tags=["work with users"], prefix="/api/auth")


async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UserService: # noqa
    return UserService(uow)


@router.post("/register")
async def register(user: UserCreateParameters,
                   user_service: UserService = Depends(get_user_service)) -> UserCreateResponse:  # noqa
    """Регистрация пользователя"""
    access_token, refresh_token = await user_service.register(
        username=user.name, password=user.password, email=user.email, role=user.role,
    )
    response = UserCreateResponse(refresh_token=refresh_token, access_token=access_token, token_type="bearer")
    return response
