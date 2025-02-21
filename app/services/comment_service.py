from fastapi import HTTPException

from app.api.schemas.comment_schema import CommentCreateParametrs, CommentReturn
from app.utils.unitofwork import IUnitOfWork


class CommentService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_comment(self, user_id: int, comment: CommentCreateParametrs):
        async with self.uow:
            await self.uow.comments.add_comment(user_id=user_id, text=comment.text, rating=comment.rating,
                                                answer=comment.answer, route_id=comment.route_id)
            await self.uow.commit()
