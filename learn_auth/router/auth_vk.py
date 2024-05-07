import json

from fastapi import APIRouter, Request, Response
from starlette.responses import RedirectResponse

from base.annotated import VKAuthDeps

from base.annotated import UserDeps, SessionDeps
from infrastructure.models.session import Session
from infrastructure.models.user import User

from base.exception import ErrorInProcessAuthException
from util.auth import create_session

router = APIRouter()


@router.get('/login')
async def login_route(
        request: Request,
        vk_auth_deps: VKAuthDeps,
        redirect_url: str
):
    local_redirect_url = str(request.url_for('auth_route'))
    result = vk_auth_deps.create_register_url(local_redirect_url)
    result_response = RedirectResponse(url=result)
    result_response.set_cookie('redirect_url', redirect_url)
    return result_response


@router.get('/auth')
async def auth_route(
        request: Request,
        response: Response,
        payload: str,
        vk_auth_deps: VKAuthDeps,
        user_deps: UserDeps,
        session_deps: SessionDeps
):
    get_redirect_url = request.cookies.get('redirect_url')
    if get_redirect_url is None:
        get_redirect_url = str(request.url_for('/'))
    result_response = RedirectResponse(url=get_redirect_url)
    result_response.delete_cookie('redirect_url')
    try:
        json_dict = json.loads(payload)
        silent_token = json_dict['token']
    except:
        raise ErrorInProcessAuthException()
    vk_id = vk_auth_deps.get_user_id_by_silent_token(silent_token)

    get_user_by_vk_id = await user_deps.get_user(vk_id=vk_id)
    user_id = None
    if get_user_by_vk_id is None:
        create_user = User.create(vk_id=vk_id)
        await user_deps.add_user(create_user)
        await user_deps.commit()
        user_id = create_user.id
    else:
        user_id = get_user_by_vk_id.id
    await create_session(response, get_user_by_vk_id.id, session_deps)
    return result_response
