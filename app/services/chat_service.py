from app.utils.unitofwork import IUnitOfWork


class ChatService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def save_message(self, from_user: int, to_user: int, message: str, files: list | None = None):
        async with self.uow:
            await self.uow.chats.add_message(from_user=from_user, to_user=to_user, message=message, files=files)
            await self.uow.commit()

    async def get_all_to_user(self, to_user: int):
        async with self.uow:
            data = await self.uow.chats.find_all_by(**{"to_user": to_user})
            self.uow.session.expunge_all()
            return data
