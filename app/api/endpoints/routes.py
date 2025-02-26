import os
from typing import Annotated
from typing import Literal
from io import BytesIO

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status
from fastapi.responses import FileResponse, StreamingResponse
import aiofile

from app.api.schemas import AllRouteReturn
from app.api.schemas import RouteCreateParameters
from app.api.schemas import RouteReturn
from app.api.schemas import RouteReturnNoContentBlocks
from app.api.schemas import RouteUpdateParameters
from app.services import RouteService
from app.utils import get_jwt_payload
from app.utils import IUnitOfWork
from app.utils import UnitOfWork

router = APIRouter(tags=["Working with map routes"], prefix="/routes")


async def get_route_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> RouteService:  # noqa
    return RouteService(uow)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(jwt_access: Annotated[str, Depends(get_jwt_payload)], route: RouteCreateParameters,
                 service: RouteService = Depends(get_route_service)) -> int:  # noqa
    """Создание маршрута"""
    return await service.create_route(int(jwt_access["sub"]), route.title)


@router.post("/update", status_code=status.HTTP_200_OK)
async def update(jwt_access: Annotated[str, Depends(get_jwt_payload)], route: RouteUpdateParameters,
                 service: RouteService = Depends(get_route_service)):  # noqa
    """Изменение Маршрута. В качестве route_id используется main_route_id"""
    await service.update(route, int(jwt_access["sub"]))


@router.get("/get_by_main_route_id_private")
async def get_private(route_id: int, jwt_access: Annotated[str, Depends(get_jwt_payload)],
                      service: RouteService = Depends(get_route_service)) -> list[RouteReturn]:  # noqa
    """Получение приватного маршрутов пользователя."""
    route = await service.get_private_route_by_id(route_id, user_id=int(jwt_access["sub"]))
    return route


@router.get("/get_by_main_route_id_public")
async def get_public(route_id: int, service: RouteService = Depends(get_route_service)) -> RouteReturn:  # noqa
    """Получение одного публичного маршрута"""
    route = await service.get_public_route_by_id(route_id)
    return route


@router.get('/all_public_routes')
async def get_all_routes(service: RouteService = Depends(get_route_service)) -> list[AllRouteReturn]:  # noqa
    """Получение всех публичных маршрутов"""
    routes = await service.get_all_public_routes()
    return routes


@router.get('/all_user_routes')
async def get_all_user_routes(user_id: int, jwt_access: Annotated[str, Depends(get_jwt_payload)],
                              service: RouteService = Depends(get_route_service)) -> list[ # noqa
    RouteReturnNoContentBlocks]:  # noqa
    """Получение всех приватных и публичных маршрутов пользователя. Для запроса нужен токен."""
    routes = await service.get_all_user_routes(user_id=user_id, user=int(jwt_access["sub"]))
    return routes


@router.get('/all_user_public_routes')
async def get_all_user_public_routes(user_id: int, service: RouteService = Depends(get_route_service)) -> list[ # noqa
    RouteReturnNoContentBlocks]:  # noqa
    """Получение всех опубликованных маршрутов пользователя"""
    routes = await service.get_all_user_public_routes(user_id)
    return routes


@router.post("/publication_request/", status_code=status.HTTP_200_OK)
async def publication_request(jwt_access: Annotated[str, Depends(get_jwt_payload)], route_id: Annotated[int, Query()], # noqa
                              service: RouteService = Depends(get_route_service)): # noqa
    """Отправка маршрута на проверку. В качестве route_id передавать main_route_id"""
    await service.publication_request(route_id, int(jwt_access["sub"]))


@router.delete('/delete_route')
async def delete_route(jwt_access: Annotated[str, Depends(get_jwt_payload)], route_id: Annotated[int, Query()], # noqa
                       service: RouteService = Depends(get_route_service)): # noqa
    """Удаление маршрута. В качестве route_id передавать main_route_id"""
    await service.delete_route(route_id=route_id, user_id=int(jwt_access["sub"]))


@router.get("/export")
async def export(route_id: int, format: Literal["gpx", "kml"], service: RouteService = Depends(get_route_service)):
    available_convertions = {"gpx": service.export_to_gpx}
    xml = await available_convertions[format](route_id, 1)
    file = BytesIO(xml[0].encode("utf-8"))
    file.seek(0)
    filename = xml[1]
    return StreamingResponse(file, media_type="application/xml", headers={"Content-Disposition": f"attachment; filename={filename}.gpx"})

