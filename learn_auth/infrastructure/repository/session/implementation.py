from typing import List
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models.session import Session
from infrastructure.repository.session.interface import ISessionRepo


class SessionRepo(ISessionRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_session(self, session: Session) -> Session:
        self.session.add(session)
        return session

    async def set_un_active_session_key(self, id_session: UUID):
        stmt_get_session = select(Session).where(Session.id == id_session)
        result_get_session = await self.session.scalar(stmt_get_session)
        if result_get_session is None:
            raise Exception()
        result_get_session.is_active = False
        await self.session.merge(result_get_session)
        await self.session.flush()

    async def session_list(self, user_id: UUID) -> List[Session]:
        stmt = select(Session).where(Session.user_id == user_id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_session_by_session_key(self, session_key: str, active: bool = True) -> Session | None:
        stmt = select(Session).where(
            and_(
                Session.session_key == session_key,
                Session.is_active == active
            )
        )
        r = await self.session.scalar(stmt)
        return r

    async def commit(self):
        await self.session.commit()
