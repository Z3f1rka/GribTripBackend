# flake8: noqa
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from app.api.schemas import AllRouteReturn
from app.api.schemas import RouteCreateParameters
from app.api.schemas import RouteReturn
from app.api.schemas import RouteReturnNoContentBlocks
from app.api.schemas import RouteUpdateParameters
from app.services import AdminService
from app.utils import get_jwt_payload
from app.utils import IUnitOfWork
from app.utils import UnitOfWork

router = APIRouter(tags=["Administrational functions"], prefix="/admin")


async def get_admin_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> AdminService:  # noqa
    return AdminService(uow)


@router.post("/approve_route", status_code=status.HTTP_200_OK)
async def approve_route(route_id: Annotated[int, Query()],  jwt_access: Annotated[str, Depends(get_jwt_payload)],
                        service: AdminService = Depends(get_admin_service)):
    """Разрешение админа на публкацию. В качестве route_id использовать main_route_id"""
    if jwt_access["role"] != "admin":
        print(jwt_access["role"])
        raise HTTPException(403, "У пользователя нет прав администратора")
    await service.approve(route_id, int(jwt_access["sub"]))