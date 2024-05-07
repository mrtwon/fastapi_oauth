from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Request, Response, Depends

from base.annotated import SessionDeps

from base.schema import SessionItem

from infrastructure.models.user import User
from util.auth import get_current_user


router = APIRouter()


@router.get('/logout')
async def logout_route(
        request: Request,
        response: Response,
        session_deps: SessionDeps
):
    session_key = request.cookies.get('session_key')
    if session_key is None:
        raise Exception()
    get_session = await session_deps.get_session_by_session_key(session_key)
    if get_session is None:
        raise Exception()
    await session_deps.set_un_active_session_key(get_session.id)
    await session_deps.commit()
    response.delete_cookie('session_key')
    return 'ok'


@router.get('/end_session')
async def end_session_route(
        session_id: UUID,
        session_deps: SessionDeps
):
    await session_deps.set_un_active_session_key(session_id)
    await session_deps.commit()
    return 'ok'


@router.get('/session_list')
async def session_list_route(
        session_deps: SessionDeps,
        current_user: Annotated[User, Depends(get_current_user)]
):
    r = await session_deps.session_list(current_user.id)
    return [SessionItem.model_validate(one) for one in r]


@router.get('/me')
async def me_route(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return f"your user id is {current_user.id}"
