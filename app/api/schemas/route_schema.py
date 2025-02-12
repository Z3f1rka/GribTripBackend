from datetime import datetime

from pydantic import BaseModel  # noqa: F401
from pydantic import ConfigDict


class RouteCreateParameters(BaseModel):
    title: str


class ContentBlocks(BaseModel):
    text: str | None = None
    title: str | None = None
    position: int
    geoposition: tuple[float, float]
    images: list | None = None


class RouteGetOne(BaseModel):
    route_id: int
    title: str
    description: str | None = None
    status: str
    photo: str | None = None
    created_at: datetime
    rating: int
    version: int


class RouteUpdateParameters(BaseModel):
    title: str
    description: str | None = None
    photo: str | None = None
    content_blocks: ContentBlocks | None = None
    route_id: int


class RouteReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None = None
    approved_id: int
    status: str
    photo: str | None = None
    created_at: datetime
    rating: int
    main_route_id: int
    version: int
    route_id: int
    user_id: int
    content_blocks: ContentBlocks | None = None
