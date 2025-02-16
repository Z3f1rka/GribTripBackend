from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class ContentBlocks(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str | None = None
    title: str | None = None
    position: int
    geoposition: tuple[float, float]
    images: list | None = None


# TODO: починить
class Route(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str | None = None
    photo: str | None = None
    content_blocks: list[ContentBlocks] | None = []

    """@field_validator('content_blocks', mode='before')
    def check(cls, content_blocks):
        print(content_blocks)
        if not content_blocks:
            content_blocks = [{'position': 1, 'geoposition': (0.0, 0.0)}]
            return"""


class RouteCreateParameters(BaseModel):
    title: Optional[str]


class RouteReturn(Route):
    model_config = ConfigDict(from_attributes=True)
    approved_id: int | None = None
    status: str
    created_at: datetime
    rating: int
    main_route_id: int
    user_id: int
    version: int


class RouteUpdateParameters(Route):
    main_route_id: int


class PrivateRouteReturn(RouteReturn):
    version: int
