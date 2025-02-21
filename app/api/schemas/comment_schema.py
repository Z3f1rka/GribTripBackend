from pydantic import BaseModel
from datetime import datetime

class CommentCreateParametrs(BaseModel):
    text: str | None = None
    rating: int
    answer: bool | None = False
    user_id: int
    route_id: int


class CommentReturn(CommentCreateParametrs):
    id: int
    created_at: datetime
