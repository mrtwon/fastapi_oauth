from typing import Annotated

from fastapi import Depends

from auth.google.interface import IGoogleAuth
from infrastructure.repository.session.interface import ISessionRepo
from infrastructure.repository.token.interface import ITokenRepo
from infrastructure.repository.user.interface import IUserRepo

from infrastructure.repository.session.interface import ISessionRepo

from auth.vk.interface import IVKAuth

UserDeps = Annotated[IUserRepo, Depends()]
TokenDeps = Annotated[ITokenRepo, Depends()]
SessionDeps = Annotated[ISessionRepo, Depends()]

GoogleAuthDeps = Annotated[IGoogleAuth, Depends()]
VKAuthDeps = Annotated[IVKAuth, Depends()]