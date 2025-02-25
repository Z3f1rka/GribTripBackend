from fastapi import HTTPException

from app.api.schemas.comment_schema import CommentCreateParametrs
from app.api.schemas.comment_schema import CommentReturn
from app.utils.unitofwork import IUnitOfWork


class CommentService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_comment(self, user_id: int, comment: CommentCreateParametrs):
        async with self.uow:
            try:
                route = await self.uow.routes.find_one(id=comment.route_id)
            except Exception:
                raise HTTPException(400, "Маршрут для комментирования не найден")
            if route.user_id == user_id:
                raise HTTPException(403, "Маршрут для комментирования не доступен")
            await self.uow.comments.add_comment(user_id=user_id, text=comment.text, rating=comment.rating,
                                                answer=comment.answer, main_route_id=comment.route_id,
                                                type=comment.type)
            await self.uow.commit()

    async def get_all_user_comments(self, user_id: int):
        async with self.uow:
            comments = await self.uow.comments.get_all_user_comments(user_id=user_id)
            for i in comments:
                i.user = await self.uow.users.find_one(id=i.user_id)
            return [CommentReturn.model_validate(i) for i in comments]

    async def get_all_route_public_comments(self, route_id: int):
        async with self.uow:
            try:
                await self.uow.routes.find_one(id=route_id)
            except Exception:
                raise HTTPException(400, "Такого маршрута не существует")
            comments = await self.uow.comments.get_all_route_public_comments(route_id=route_id)
            for i in comments:
                i.user = await self.uow.users.find_one(id=i.user_id)
            return [CommentReturn.model_validate(i) for i in comments]

    async def delete_comment(self, user_id: int, comment_id: int):
        async with self.uow:
            try:
                comment = await self.uow.comments.find_one(id=comment_id)
            except Exception:
                raise HTTPException(400, "Такого комментария не существует")
            if comment.user_id != user_id:
                raise HTTPException(403, "Пользователь не является автором комментария")
            await self.uow.comments.del_one(id=comment_id)
            await self.uow.commit()
