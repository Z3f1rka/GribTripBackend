from app.db.models import Route
from app.repositories.basic_repo import Repository


class RouteRepository(Repository):
    model = Route

    async def add_route(self, user_id: int, title: str):
        await super().add_one({"user_id": user_id, "title": title})
        