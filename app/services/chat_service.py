from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from app.api.schemas import AllRouteReturn
from app.api.schemas import CommentCreateParametrs
from app.api.schemas import RouteReturn
from app.utils.unitofwork import IUnitOfWork


class ChatService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def save_message(self, from_user: int, to_user: int, message: str, files: list | None = None):
        async with self.uow:
            await self.uow.chats.add_message(from_user=from_user, to_user=to_user, message=message, files=files)
            await self.uow.commit()
