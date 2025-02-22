from sqlalchemy import insert
from sqlalchemy import select

from app.db.models import Comment
from app.repositories.basic_repo import Repository


class CommentRepository(Repository):
    model = Comment

    async def add_comment(self, user_id: int, text: str, rating: int, route_id: int, answer: bool | None = False):
        stmt = insert(self.model).values(**{"user_id": user_id, "text": text, "rating": rating,
                                            "route_id": route_id, "answer": answer}).returning(self.model)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_all_user_comments(self, user_id):
        stmt = select(self.model).where(self.model.user_id == user_id)
        comments = await self.session.execute(stmt)
        comments = comments.scalars().all()
        return comments

    async def get_all_route_comments(self, route_id):
        stmt = select(self.model).where(self.model.route_id == route_id)
        comments = await self.session.execute(stmt)
        comments = comments.scalars().all()
        return comments
