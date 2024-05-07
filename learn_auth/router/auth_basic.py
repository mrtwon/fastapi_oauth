import hashlib
from typing import Annotated

from fastapi import APIRouter, Response, Depends

from base.annotated import UserDeps, SessionDeps
from base.schema import CreateBasicUserSchema, LoginBasicUserSchema
from infrastructure.models.user import User

from infrastructure.models.session import Session

from base.exception import UserAlreadyExist, InvalidEmailPasswordException
from util.auth import create_session, get_md5

router = APIRouter()


@router.post('/register')
async def register_user_route(
        user_deps: UserDeps,
        schema: CreateBasicUserSchema
):
    r: User | None = await user_deps.get_user(email=schema.email)
    if r is not None:
        raise UserAlreadyExist()
    md5_password = get_md5(schema.password)
    create_user = User.create(email=schema.email, password=md5_password)
    added_user: User = await user_deps.add_user(create_user)
    await user_deps.commit()
    return added_user.id


@router.post('/login')
async def login_user_route(
        response: Response,
        user_deps: UserDeps,
        session_deps: SessionDeps,
        schema: LoginBasicUserSchema
):
    md5_password = get_md5(schema.password)
    get_user = await user_deps.get_user_by_pass_email(email=schema.email, password=md5_password)
    if get_user is None:
        raise InvalidEmailPasswordException()
    await create_session(response, get_user.id, session_deps)
    return 'ok'


class Test:
    def __init__(self, select_user: bool):
        self.select_user = select_user

    def __call__(self, *args, **kwargs):
        return 'ok!'


@router.get('/test')
async def test(test: Annotated[str, Depends(Test(True))]):
    return test
