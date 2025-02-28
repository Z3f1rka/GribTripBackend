from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from app.api.schemas.user_schemas import UserGetResponse


class CommentCreateParametrs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str | None = None
    rating: int = 0
    answer: bool | None = False
    route_id: int
    type: str | None = 'public'


class CommentReturn(CommentCreateParametrs):
    id: int
    created_at: datetime
    user: UserGetResponse
