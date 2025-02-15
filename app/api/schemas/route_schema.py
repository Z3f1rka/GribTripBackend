from datetime import datetime
from typing import List, Optional


from pydantic import BaseModel
from pydantic import ConfigDict, field_validator


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
    content_blocks:  list[ContentBlocks | None] | None = None

    @field_validator('content_blocks', mode='before')
    def check(cls, content_blocks):
        if not content_blocks:
            return [{'position': 1, 'geoposition': (0.0, 0.0)}]


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


class RouteUpdateParameters(Route):
    main_route_id: int

class PrivateRoute(BaseModel):
    versions: List[RouteReturn]
