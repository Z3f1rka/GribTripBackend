from app.db.models import Session
from app.repositories.basic_repo import Repository


class SessionRepository(Repository):
    model = Session

    async def add_token(self, user_id: int, jwt: str, useragent: str | None = None):
        await super().add_one({"user_id": user_id, "jwt_refresh": jwt, "useragent": useragent})
