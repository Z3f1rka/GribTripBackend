from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ContentBlocks(BaseModel):
    text: str | None = None
    title: str | None = None
    position: int
    geoposition: tuple[float, float]
    images: list | None = None


class Route(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str | None = None
    photo: str | None = None
    content_blocks: ContentBlocks | None = None


class RouteCreateParameters(BaseModel):
    title: str


class RouteReturn(Route):
    model_config = ConfigDict(from_attributes=True)
    approved_id: int | None = None
    status: str
    created_at: datetime
    rating: int
    main_route_id: int
    version: int
    user_id: int


class RouteUpdateParameters(Route):
    route_id: int
    version: int
