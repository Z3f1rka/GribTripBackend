from datetime import datetime

from pydantic import BaseModel


class RouteCreateParameters(BaseModel):
    title: str


class RouteGetOne(BaseModel):
    route_id: int
    title: str
    description: str | None = None
    status: str
    photo: str | None = None
    created_at: datetime
    rating: int
    main_route_id: int | None = None
    version: int
    content_blocks: dict | None = None


class RouteUpdateParameters(BaseModel):
    title: str
    description: str | None = None
    photo: str | None = None
    content_blocks: dict | None = None
    route_id: int


class RouteUpdateReturn(BaseModel):
    title: str
    description: str | None = None
    photo: str | None = None
    content_blocks: dict | None = None
    main_route_id: int
    route_id: int


class ContentBlocks(BaseModel):
    text: str | None = None
    title: str | None = None
    position: int
    geoposition: (float, float)
    images: list | None = None
