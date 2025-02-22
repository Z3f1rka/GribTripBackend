from fastapi import HTTPException

from app.api.schemas.comment_schema import CommentCreateParametrs
from app.api.schemas.comment_schema import CommentReturn
from app.utils.unitofwork import IUnitOfWork


class CommentService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_comment(self, user_id: int, comment: CommentCreateParametrs):
        async with self.uow:
            await self.uow.comments.add_comment(user_id=user_id, text=comment.text, rating=comment.rating,
                                                answer=comment.answer, route_id=comment.route_id)
            await self.uow.commit()

    async def get_all_user_comments(self, user_id: int):
        async with self.uow:
            comments = await self.uow.comments.get_all_user_comments(user_id=user_id)
            return [CommentReturn.model_validate(i) for i in comments]

    async def get_all_route_comments(self, route_id: int):
        async with self.uow:
            try:
                await self.uow.routes.find_one(id=route_id)
            except Exception:
                raise HTTPException(400, "Такого маршрута не существует")
            comments = await self.uow.comments.get_all_route_comments(route_id=route_id)
            return [CommentReturn.model_validate(i) for i in comments]
