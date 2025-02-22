from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class CommentCreateParametrs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str | None = None
    rating: int | None = None
    answer: bool | None = False
    route_id: int
    type: str | None = 'public'


class CommentReturn(CommentCreateParametrs):
    id: int
    created_at: datetime
