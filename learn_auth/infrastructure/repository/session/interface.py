from typing import Protocol, List
from uuid import UUID

from infrastructure.models.session import Session


class ISessionRepo(Protocol):
    async def add_session(self, session: Session) -> Session:
        raise NotImplementedError

    async def set_un_active_session_key(self, id_session: UUID):
        raise NotImplementedError

    async def session_list(self, user_id: UUID) -> List[Session]:
        raise NotImplementedError

    async def get_session_by_session_key(self, session_key: str) -> Session | None:
        raise NotImplementedError
