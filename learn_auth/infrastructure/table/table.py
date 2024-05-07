from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, UUID, ForeignKey, TIMESTAMP
from sqlalchemy.orm import registry

from infrastructure.models.user import User

from infrastructure.models.session import Session

mapper_registry = registry()

user = Table(
    "user",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("email", String, nullable=True),
    Column("password", String, nullable=True),
    Column("google_id", String, nullable=True),
    Column('vk_id', Integer, nullable=True),
    Column("is_verify", Boolean, default=False)
)

session = Table(
    "session",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("user.id")),
    Column("session_key", String, nullable=False),
    Column("create_at", TIMESTAMP, nullable=False),
    Column("is_active", Boolean, default=True)
)


def map_user():
    mapper_registry.map_imperatively(
        User,
        user
    )


def map_session():
    mapper_registry.map_imperatively(
        Session,
        session
    )
