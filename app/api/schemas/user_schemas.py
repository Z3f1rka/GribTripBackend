from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserCreateResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UserCreateParameters(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"


class UserLogInParameters(BaseModel):
    email: EmailStr
    password: str


class UserLogInResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UserGetMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    avatar: str | None = None
