from typing import Annotated

from fastapi import APIRouter, status
from fastapi import Depends

from app.api.schemas import RouteCreateParameters
from app.api.schemas import RouteReturn, PrivateRoute
from app.api.schemas import RouteUpdateParameters
from app.services.route_service import RouteService
from app.utils import get_jwt_payload
from app.utils import IUnitOfWork
from app.utils import UnitOfWork

router = APIRouter(tags=["Working with map routes"], prefix="/api/routes")


async def get_route_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> RouteService:
    return RouteService(uow)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(jwt_access: Annotated[str, Depends(get_jwt_payload)], route: RouteCreateParameters,
                 service: RouteService = Depends(get_route_service)):
    await service.create_route(int(jwt_access["sub"]), route.title)


@router.post("/update", status_code=status.HTTP_200_OK)
async def update(jwt_access: Annotated[str, Depends(get_jwt_payload)], route: RouteUpdateParameters,
                 service: RouteService = Depends(get_route_service)):
    """В качестве route_id используется main_route_id"""
    await service.update(route, int(jwt_access["sub"]))


@router.get("/get_by_id_private")
async def get(route_id: int, jwt_access: Annotated[str, Depends(get_jwt_payload)], service: RouteService = Depends(get_route_service)):
    route = await service.get_route_by_id(route_id, user_id=int(jwt_access["sub"]))
    return route
