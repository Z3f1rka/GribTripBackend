from pydantic import BaseModel


class RouteCreateParameters(BaseModel):
    title: str


class RouteUpdateParameters(BaseModel):
    title: str
    description: str | None = None
    photo: str | None = None
    content_blocks: dict | None = None


class RouteUpdateReturn(BaseModel):
    title: str
    description: str | None = None
    photo: str | None = None
    content_blocks: dict | None = None


class ContentBlocks(BaseModel):
    text: str | None = None
    title: str | None = None
    position: int
    geoposition: (float, float)
    images: list | None = None
