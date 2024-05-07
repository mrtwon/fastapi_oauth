import hashlib
from uuid import UUID

from fastapi import Request, Response

from base.annotated import SessionDeps, UserDeps
from infrastructure.models.session import Session
from infrastructure.models.user import User

from base.annotated import GoogleAuthDeps, TokenDeps

from base.exception import NotAuthException, SessionNotFoundException, UserNotFoundException, \
    ErrorInProcessAuthException, SessionAlreadyFinish


async def get_google_user(
        request: Request,
        response: Response,
        user_deps: UserDeps,
        google_auth_deps: GoogleAuthDeps,
        token_deps: TokenDeps
) -> User:
    google_access_token = request.cookies.get('google_access_token')
    refresh_token = token_deps.get_refresh_token(google_access_token)
    if refresh_token is None:
        response.delete_cookie('google_access_token')
        raise SessionAlreadyFinish()
    info_by_token = google_auth_deps.get_info_by_token(google_access_token)
    if info_by_token is None:
        new_access_token = google_auth_deps.get_new_access_token(refresh_token)
        if new_access_token is None:
            raise ErrorInProcessAuthException()
        token_deps.update_token(google_access_token, new_access_token)
        response.set_cookie('google_access_token', new_access_token)
        info_by_token = google_auth_deps.get_info_by_token(new_access_token)
        if info_by_token is None:
            raise ErrorInProcessAuthException()
        get_user_by_id = await user_deps.get_user(google_id=info_by_token.sub)
        if get_user_by_id is None:
            raise UserNotFoundException()
        return get_user_by_id
    else:
        get_user_by_id = await user_deps.get_user(google_id=info_by_token.sub)
        return get_user_by_id


async def get_session_user(
        request: Request,
        user_deps: UserDeps,
        session_deps: SessionDeps
) -> User:
    session_key = request.cookies.get('session_key')
    if not session_key:
        raise NotAuthException()
    get_session: Session | None = await session_deps.get_session_by_session_key(session_key)
    if not get_session:
        raise SessionNotFoundException()
    get_user: User | None = await user_deps.get_user(user_id=get_session.user_id)
    if not get_user:
        raise UserNotFoundException()
    return get_user


async def get_current_user(
        request: Request,
        response: Response,
        session_deps: SessionDeps,
        user_deps: UserDeps,
        google_auth_deps: GoogleAuthDeps,
        token_deps: TokenDeps
) -> User:
    if request.cookies.get('session_key'):
        return await get_session_user(
            request,
            user_deps,
            session_deps
        )
    elif request.cookies.get('google_access_token'):
        return await get_google_user(
            request,
            response,
            user_deps,
            google_auth_deps,
            token_deps
        )
    else:
        raise NotAuthException()


async def create_session(response: Response, user_id: UUID, session_deps: SessionDeps):
    new_session = Session.create(user_id)
    await session_deps.add_session(new_session)
    await session_deps.commit()
    response.set_cookie('session_key', new_session.session_key)


def get_md5(input_value: str) -> str:
    return hashlib.md5(input_value.encode()).hexdigest()
