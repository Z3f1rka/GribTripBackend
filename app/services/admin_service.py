from fastapi import HTTPException

from app.utils.unitofwork import IUnitOfWork


class AdminService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def approve(self, id: int, user_id: int):
        async with self.uow:
            user = await self.uow.users.find_one(id=user_id)
            if user.role != "admin":
                raise HTTPException(403, "У пользователя нет прав администратора")
            await self.uow.admins.approve(id, user_id)
            await self.uow.commit()


if __name__ == "__main__":
    pass
