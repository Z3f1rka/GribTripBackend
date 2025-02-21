from pydantic import BaseModel
from datetime import datetime
from pydantic import ConfigDict

class CommentCreateParametrs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str | None = None
    rating: int
    answer: bool | None = False
    route_id: int


class CommentReturn(CommentCreateParametrs):
    id: int
    created_at: datetime
