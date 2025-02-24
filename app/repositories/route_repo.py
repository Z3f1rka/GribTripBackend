from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from app.db.models import Comment
from app.db.models import Route
from app.repositories.basic_repo import Repository
from app.utils.rating_formula import rating_calculation


class RouteRepository(Repository):
    model = Route

    async def add_route(self, user_id: int, title: str):
        stmt = insert(self.model).values(**{"user_id": user_id, "title": title}).returning(self.model)
        route = await self.session.execute(stmt)
        route_id = route.scalar_one().id
        stmt = update(self.model).where(self.model.id == route_id).values(main_route_id=route_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return route_id

    async def update(self, title: str, main_route_id: int, description: str | None = None, photo: str | None = None,
                     content_blocks: list | None = None):
        stmt = select(self.model).where(self.model.main_route_id == main_route_id).order_by(self.model.version.desc())
        route = await self.session.execute(stmt)
        route = route.scalars().first()
        version = route.version
        if not description:
            description = route.description
        if not photo:
            photo = route.photo
        if not content_blocks:
            content_blocks = route.content_blocks
        stmt = insert(self.model).values(**{"title": title,
                                            "description": description,
                                            "photo": photo,
                                            "content_blocks": content_blocks,
                                            "version": version + 1,
                                            "main_route_id": main_route_id,
                                            "user_id": route.user_id})
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_by_main_route_id_private(self, main_route_id: int):
        stmt = select(self.model).where(self.model.main_route_id == main_route_id).order_by(self.model.version.desc())
        route = await self.session.execute(stmt)
        route = route.scalars().all()
        stmt = select(Comment).where(Comment.route_id == main_route_id, Comment.type == "public")
        comments = await self.session.execute(stmt)
        comments = comments.scalars().all()
        if comments:
            comments = [(i.created_at, i.rating) for i in comments]
            for i in route:
                i.rating = rating_calculation(comments)
        return route

    async def find_by_main_route_id_public(self, main_route_id: int):
        stmt = select(self.model).where(self.model.main_route_id == main_route_id,
                                        self.model.status == "public").order_by(
            self.model.version.desc())
        route = await self.session.execute(stmt)
        route = route.scalars().first()
        stmt = select(Comment).where(Comment.route_id == main_route_id, Comment.type == "public")
        comments = await self.session.execute(stmt)
        comments = comments.scalars().all()
        if not comments:
            route.rating = 0
        else:
            comments = [(i.created_at, i.rating) for i in comments]
            route.rating = rating_calculation(comments)
        return route

    async def find_all_public_routes(self):
        stmt = select(self.model.main_route_id).group_by(self.model.main_route_id)
        main_route_id = await self.session.execute(stmt)
        main_route_id = main_route_id.scalars().all()
        routes = []
        for id in main_route_id:
            stmt = select(self.model).where(self.model.main_route_id == id, self.model.status == "public").order_by(
                self.model.version.desc())
            route = await self.session.execute(stmt)
            route = route.scalars().first()
            if route:
                routes.append(route)
        return routes

    async def find_all_user_routes(self, user_id):
        stmt = select(self.model.main_route_id).where(self.model.user_id == user_id).group_by(self.model.main_route_id)
        main_route_id = await self.session.execute(stmt)
        main_route_id = main_route_id.scalars().all()
        routes = []
        for id in main_route_id:
            stmt = select(self.model).where(self.model.main_route_id == id).order_by(self.model.version.desc())
            route = await self.session.execute(stmt)
            route = route.scalars().first()
            stmt = select(Comment).where(Comment.route_id == id, Comment.type == "public")
            comments = await self.session.execute(stmt)
            comments = comments.scalars().all()
            if not comments:
                route.rating = 0
            else:
                comments = [(i.created_at, i.rating) for i in comments]
                route.rating = rating_calculation(comments)
            routes.append(route)
        return routes

    async def find_all_user_public_routes(self, user_id):
        routes = await self.find_all_user_routes(user_id)
        for_return = []
        for route in routes:
            if route.status == 'public':
                stmt = select(Comment).where(Comment.route_id == route.main_route_id, Comment.type == "public")

                comments = await self.session.execute(stmt)
                comments = comments.scalars().all()
                if not comments:
                    route.rating = 0
                else:
                    comments = [(i.created_at, i.rating) for i in comments]
                    route.rating = rating_calculation(comments)
                for_return.append(route)
        return for_return

    async def change_status(self, id: int, status: str):
        stmt = select(self.model).where(self.model.main_route_id == id).order_by(self.model.version.desc())
        route = await self.session.execute(stmt)
        route = route.scalars().first()
        route.status = status
        self.session.add(route)
