from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.api.schemas import RouteReturnNoContentBlocks
from app.services import HistoryService
from app.utils import get_jwt_payload
from app.utils import IUnitOfWork
from app.utils import UnitOfWork

router = APIRouter(tags=["Working with history"], prefix="/history")


async def get_history_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> HistoryService:  # noqa
    return HistoryService(uow)


@router.get('/routes')
async def history(jwt_access: Annotated[str, Depends(get_jwt_payload)], service: HistoryService = Depends(get_history_service)) -> list[RouteReturnNoContentBlocks]: # noqa
    """Получение всех маршрутов, которые пользователь посещал"""
    history = await service.history(int(jwt_access["sub"]))
    return history
