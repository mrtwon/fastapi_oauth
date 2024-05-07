from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models.user import User
from infrastructure.repository.user.base import SQLAlchemyInterface
from infrastructure.repository.user.interface import IUserRepo


class UserRepo(IUserRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        return user

    async def get_user(self, user_id: UUID | None = None, google_id: str | None = None,
                       email: str | None = None, vk_id: str | None = None) -> User:
        stmt = None
        if user_id:
            stmt = select(User).where(User.id == user_id)
        elif google_id:
            stmt = select(User).where(User.google_id == google_id)
        elif email:
            stmt = select(User).where(User.email == email)
        elif vk_id:
            stmt = select(User).where(User.vk_id == vk_id)
        else:
            raise Exception()
        r = await self.session.scalar(stmt)
        return r

    async def get_user_by_pass_email(self, email: str, password: str) -> User | None:
        stmt = select(User).where(and_(User.email == email, User.password == password))
        r = await self.session.scalar(stmt)
        return r

    async def commit(self):
        await self.session.commit()
