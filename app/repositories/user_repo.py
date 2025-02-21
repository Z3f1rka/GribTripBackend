from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.repositories.basic_repo import Repository
from app.utils import get_password_hash


class UserRepository(Repository):
    model = User

    async def add_user(self, username: str, email: str, password: str):
        try:
            result = await super().add_one(
                {"username": username, "email": email, "hashed_password": get_password_hash(password), "role": "user"},
            )
            return result.id
        except IntegrityError:
            raise HTTPException(400, "Пользователь уже существует")
