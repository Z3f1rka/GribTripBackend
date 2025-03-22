from sqlalchemy import insert

from app.db.models import Message
from app.repositories.basic_repo import Repository


class ChatRepository(Repository):
    model = Message

    async def add_message(self, from_user: int, to_user: int, message: str, files: list | None = None):
        stmt = insert(self.model).values(from_user=from_user, to_user=to_user, text=message, files=files)
        await self.session.execute(stmt)
