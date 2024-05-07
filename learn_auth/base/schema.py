from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CreateBasicUserSchema(BaseSchema):
    email: str
    password: str


class LoginBasicUserSchema(BaseSchema):
    email: str
    password: str


class SessionItem(BaseSchema):
    id: UUID
    create_at: datetime
    is_active: bool
