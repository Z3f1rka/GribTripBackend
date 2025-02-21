from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.api.schemas import CommentCreateParametrs
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
    print(comment)
    await service.create_comment(int(jwt_access["sub"]), comment)