from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from app.db.models import Comment
from app.repositories.basic_repo import Repository


class CommentRepository(Repository):
    model = Comment

    async def add_comment(self, user_id: int, text: str, rating: int, route_id: int, answer: bool | None = False):
        stmt = insert(self.model).values(**{"user_id": user_id, "text": text, "rating": rating,
                                            "route_id": route_id, "answer": answer}).returning(self.model)
        comment = await self.session.execute(stmt)
        await self.session.commit()
        