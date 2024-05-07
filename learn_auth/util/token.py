from fastapi import Response
from auth.google.interface import IGoogleAuth
from infrastructure.models.user import User
from infrastructure.repository.token.interface import ITokenRepo
from infrastructure.repository.user.interface import IUserRepo

from base.exception import ErrorInProcessAuthException


async def add_token_and_create_user(
        resp: Response,
        access_token: str,
        refresh_token: str,
        google_auth: IGoogleAuth,
        user_repo: IUserRepo,
        token_repo: ITokenRepo
):
    token_info = google_auth.get_info_by_token(access_token)
    if token_info in None:
        raise ErrorInProcessAuthException()
    user_by_google_id = await user_repo.get_user(google_id=token_info.sub)
    if user_by_google_id is None:
        user_model = User.create(google_id=token_info.sub)
        await user_repo.add_user(user_model)
        await user_repo.commit()
    token_repo.add_token(access_token, refresh_token)
    resp.set_cookie('google_access_token', access_token)
