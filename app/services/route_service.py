from fastapi import HTTPException
import gpxpy
import simplekml

from app.api.schemas.route_schema import AllRouteReturn
from app.api.schemas.route_schema import RouteReturn
from app.api.schemas.route_schema import RouteReturnNoContentBlocks
from app.api.schemas.route_schema import RouteUpdateParameters
from app.utils.unitofwork import IUnitOfWork


class RouteService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_private_route_by_id(self, id: int, user_id: int):
        async with self.uow:
            routes = await self.uow.routes.find_by_main_route_id_private(id)
            if routes:
                route = routes[-1]
                if route.user_id == user_id:
                    return [RouteReturn.model_validate(i) for i in routes]
                else:
                    raise HTTPException(403, "Пользователь не является владельцем маршрута")
            else:
                raise HTTPException(400, "Такого маршрута не существует")

    async def get_public_route_by_id(self, id: int):
        async with self.uow:
            route = await self.uow.routes.find_by_main_route_id_public(id)
            if not route:
                raise HTTPException(404, "Публичных маршрутов с этим id не существует")
            route = RouteReturn.model_validate(route)
            return route

    async def create_route(self, user_id: int, title: str):
        async with self.uow:
            route_id = await self.uow.routes.add_route(user_id=user_id, title=title)
            await self.uow.commit()
            return route_id

    async def update(self, route: RouteUpdateParameters, user_id: int):
        async with self.uow:
            db_route = await self.uow.routes.find_by_main_route_id_private(route.main_route_id)
            if not db_route:
                raise HTTPException(400, "Такого маршрута не существует")
            db_route = db_route[0]
            if db_route.user_id == user_id:
                if db_route.status == "check":
                    raise HTTPException(400, "Маршрут находится на проверке")
                else:
                    content_blocks = [i.model_dump() for i in route.content_blocks]
                await self.uow.routes.update(title=route.title, description=route.description, photo=route.photo,
                                             main_route_id=route.main_route_id,
                                             content_blocks=content_blocks)
                await self.uow.commit()
            else:
                raise HTTPException(403, "Пользователь не является владельцем маршрута")

    async def get_all_public_routes(self):
        async with self.uow:
            routes = await self.uow.routes.find_all_public_routes()
            return [AllRouteReturn.model_validate(i) for i in routes]

    async def get_all_user_routes(self, user_id: int, user: int):
        async with self.uow:
            if user_id != user:
                raise HTTPException(403, "Пользователь не является владельцем маршрутов")
            routes = await self.uow.routes.find_all_user_routes(user_id)
            return [RouteReturnNoContentBlocks.model_validate(i) for i in routes]

    async def get_all_user_public_routes(self, user_id: int):
        async with self.uow:
            routes = await self.uow.routes.find_all_user_public_routes(user_id)
            return [RouteReturnNoContentBlocks.model_validate(i) for i in routes]

    async def publication_request(self, main_route_id: int, user_id: int):
        async with self.uow:
            db_route = await self.uow.routes.find_by_main_route_id_private(main_route_id)
            if not db_route:
                raise HTTPException(400, "Такого маршрута не существует")
            if any(i.status == "check" for i in db_route):
                raise HTTPException(400, "Маршрут находится на проверке")
            db_route = db_route[0]
            if db_route.user_id == user_id:
                if db_route.status == "public":
                    raise HTTPException(400, "Маршрут уже опубликован")
                await self.uow.routes.change_status(main_route_id, "check")
                await self.uow.commit()
            else:
                raise HTTPException(403, "Пользователь не является владельцем маршрута")

    async def delete_route(self, route_id: int, user_id: int):
        async with self.uow:
            db_route = await self.uow.routes.find_by_main_route_id_private(main_route_id=route_id)
            if not db_route:
                raise HTTPException(400, "Такого маршрута не существует")
            if db_route[0].user_id != user_id:
                raise HTTPException(403, "Пользователь не является владельцем маршрута")
            for route in db_route:
                await self.uow.routes.del_one(id=route.id)
            await self.uow.commit()

    async def export_to_gpx(self, route_id: int, user_id: int):
        async with self.uow:
            try:
                db_route = (await self.uow.routes.find_by_main_route_id_private(main_route_id=route_id))[0]
            except Exception:
                raise HTTPException(400, "Такого маршрута не существует")
            if db_route.user_id != user_id:
                db_route = await self.uow.routes.find_by_main_route_id_public(route_id)
                if not db_route:
                    raise HTTPException(400, "Этот маршрут недоступен")
            gpx_obj = gpxpy.gpx.GPX()
            gpx_route = gpxpy.gpx.GPXRoute(name=db_route.title, description=db_route.description)
            if not db_route.content_blocks:
                gpx_obj.routes.append(gpx_route)
                return gpx_obj.to_xml(), db_route.title
            content_blocks = sorted(db_route.content_blocks, key=lambda x: x["position"])
            for block in content_blocks:
                gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(block["geoposition"][0], block["geoposition"][1],
                                                                name=block["title"], description=block["text"]))
            gpx_obj.routes.append(gpx_route)
            return gpx_obj.to_xml(), db_route.title

    async def export_to_kml(self, route_id: int, user_id: int):
        kml_create_params = {}
        async with self.uow:
            try:
                db_route = (await self.uow.routes.find_by_main_route_id_private(main_route_id=route_id))[0]
            except Exception:
                raise HTTPException(400, "Такого маршрута не существует")
            if db_route.user_id != user_id:
                db_route = await self.uow.routes.find_by_main_route_id_public(route_id)
                if not db_route:
                    raise HTTPException(400, "Этот маршрут недоступен")

            existing_cb = bool(db_route.content_blocks)
            kml_create_params = {"name": db_route.title, "description": db_route.description}
            if existing_cb:
                x = sum([i["geoposition"][0] for i in db_route.content_blocks]) / len(db_route.content_blocks)
                y = sum([i["geoposition"][1] for i in db_route.content_blocks]) / len(db_route.content_blocks)
                lookat = (x, y)
                kml_create_params["lookat"] = lookat
            kml = simplekml.Kml(**kml_create_params)

            if not existing_cb:
                return kml.kml(), kml_create_params["name"]
            else:
                content_blocks = sorted(db_route.content_blocks, key=lambda x: x["position"])

                points_for_line = []
                for block in content_blocks:
                    kml.newpoint(name=block["title"],
                                 description=block["text"],
                                 coords=[(block["geoposition"][1], block["geoposition"][0])])
                    points_for_line.append((block["geoposition"][1], block["geoposition"][0]))
                linestring = kml.newlinestring(name="Машрут")
                linestring.coords = points_for_line
                # kml._outputkmz()
                return kml.kml(), kml_create_params["name"]
