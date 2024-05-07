import uuid
from uuid import UUID

from attr import field

from infrastructure.models.base import entity


@entity
class User:
    id: UUID = field(default=uuid.uuid4())
    email: str
    password: str
    google_id: str
    vk_id: int
    is_verify: bool = field(default=False)

    @staticmethod
    def create(
            email: str | None = None,
            password: str | None = None,
            google_id: str | None = None,
            vk_id: int | None = None
    ):
        return User(
            email=email,
            password=password,
            google_id=google_id,
            vk_id=vk_id
        )

