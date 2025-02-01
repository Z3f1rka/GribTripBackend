from app.utils import create_token
from app.utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register(self, username: str, email: str, password: str, role: str):
        async with self.uow:
            user_id = await self.uow.users.add_user(username=username, email=email, password=password, role=role)
            access_token = create_token("access", user_id)
            refresh_token = create_token("refresh", user_id)
            await self.uow.commit()
            await self.uow.sessions.add_token(user_id=user_id, jwt=refresh_token)
            await self.uow.commit()
            return access_token, refresh_token
