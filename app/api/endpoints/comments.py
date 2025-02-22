from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.api.schemas import CommentCreateParametrs
from app.api.schemas import CommentReturn
from app.services import CommentService
from app.utils import get_jwt_payload
from app.utils import IUnitOfWork
from app.utils import UnitOfWork

router = APIRouter(tags=["Working with comments"], prefix="/comments")


async def get_comment_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> CommentService:  # noqa
    return CommentService(uow)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(jwt_access: Annotated[str, Depends(get_jwt_payload)], comment: CommentCreateParametrs,
                 service: CommentService = Depends(get_comment_service)):  # noqa
    """Создание комментария"""
    await service.create_comment(int(jwt_access["sub"]), comment)


@router.get('/get_all_user_comments')
async def get_all_user_comments(jwt_access: Annotated[str, Depends(get_jwt_payload)],
                                service: CommentService = Depends(get_comment_service)) -> list[CommentReturn]: # noqa
    """Получение всех пользовательских комментариев"""
    comments = await service.get_all_user_comments(int(jwt_access["sub"]))
    return comments


@router.get('/get_all_route_public_comments')
async def get_all_user_comments(route_id: int, service: CommentService = Depends(get_comment_service)) -> list[CommentReturn]: # noqa
    """Получение всех публичных комментариев одного маршрута"""
    comments = await service.get_all_route_public_comments(route_id)
    return comments


@router.delete('/delete')
async def delete_comment(comment_id: int, jwt_access: Annotated[str, Depends(get_jwt_payload)],
                         service: CommentService = Depends(get_comment_service)): # noqa
    """Удаление комментария"""
    await service.delete_comment(comment_id=comment_id, user_id=int(jwt_access["sub"]))
