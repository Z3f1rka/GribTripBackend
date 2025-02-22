from app.api.schemas import RouteReturnNoContentBlocks
from app.utils.unitofwork import IUnitOfWork


class HistoryService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def history(self, user_id: int):
        async with self.uow:
            history = []
            comments = await self.uow.comments.get_all_user_comments(user_id=user_id)
            for com in comments:
                route = await self.uow.routes.find_by_main_route_id_public(main_route_id=com.route_id)
                if route:
                    history.append(route)
            return [RouteReturnNoContentBlocks.model_validate(i) for i in history]
