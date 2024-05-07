import uuid
from datetime import datetime
from secrets import token_hex
from uuid import UUID

from attr import field

from infrastructure.models.base import entity


@entity
class Session:
    id: UUID = field(default=uuid.uuid4())
    user_id: UUID
    session_key: str = field(default=token_hex(64))
    is_active: bool = field(default=True)
    create_at: datetime = field(default=datetime.now())

    @staticmethod
    def create(
            user_id: UUID
    ) -> "Session":
        return Session(
            user_id=user_id
        )