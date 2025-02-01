from pydantic import BaseModel
from pydantic import EmailStr


class UserCreateResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UserCreateParameters(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogInParameters(BaseModel):
    email: EmailStr
    password: str


class UserLogInResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UserGetMeResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    is_active: bool
