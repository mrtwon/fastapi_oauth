from typing import Protocol
from uuid import UUID

from infrastructure.models.user import User


class SessionInterface:
    async def commit(self):
        raise NotImplementedError


class IUserRepo(SessionInterface):
    async def add_user(self, user: User) -> User:
        raise NotImplementedError

    async def get_user(self, user_id: UUID | None = None, google_id: str | None = None,
                       email: str | None = None, vk_id: str | None = None) -> User:
        raise NotImplementedError

    async def get_user_by_pass_email(self, email: str, password: str) -> User | None:
        raise NotImplementedError
