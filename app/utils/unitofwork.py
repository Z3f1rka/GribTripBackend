from abc import ABC
from abc import abstractmethod

from app.db.database import async_session_maker
from app.repositories import AdminRepo
from app.repositories import CommentRepository
from app.repositories import RouteRepository
from app.repositories import SessionRepository
from app.repositories import UserRepository


class IUnitOfWork(ABC):
    users: UserRepository
    sessions: SessionRepository
    routes: RouteRepository
    admins: AdminRepo
    comments: CommentRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.sessions = SessionRepository(self.session)
        self.routes = RouteRepository(self.session)
        self.admins = AdminRepo(self.session)
        self.comments = CommentRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
