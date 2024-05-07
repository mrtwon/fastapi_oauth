from fastapi import APIRouter, Request, Response
from starlette.responses import RedirectResponse

from base.annotated import UserDeps, TokenDeps, GoogleAuthDeps
from util.token import add_token_and_create_user

router = APIRouter()


@router.get('/login')
async def google_login_route(
        request: Request,
        google_auth_deps: GoogleAuthDeps,
        redirect_url: str
):
    local_redirect_url = str(request.url_for('google_auth_route'))
    result_url = google_auth_deps.create_register_url(local_redirect_url)
    response_result = RedirectResponse(url=result_url)
    response_result.set_cookie('redirect_url', redirect_url)


@router.get('/auth')
async def google_auth_route(
        code: str,
        request: Request,
        response: Response,
        user_dep: UserDeps,
        token_deps: TokenDeps,
        google_auth_deps: GoogleAuthDeps
):
    local_redirect_url = 'http://localhost/auth/google/auth'
    result = google_auth_deps.get_access_and_refresh_token(code, local_redirect_url)
    await add_token_and_create_user(
        resp=response,
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        user_repo=user_dep,
        token_repo=token_deps,
        google_auth=google_auth_deps
    )
    result_redirect_url = request.cookies.get('redirect_url')
    if result_redirect_url is None:
        result_redirect_url = str(request.url_for('/'))
    result_response = RedirectResponse(url=result_redirect_url)
    result_response.delete_cookie('redirect_url')
    return result_response


@router.get('/logout')
async def logout_google_route(
        request: Request,
        response: Response,
        token_deps: TokenDeps
):
    google_access_token = request.cookies.get('google_access_token')
    token_deps.delete_token(google_access_token)
    response.delete_cookie('google_access_token')
