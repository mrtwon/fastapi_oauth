from auth.google.model import GoogleUserInfo

from auth.google.model import GoogleAccessRefreshToken


class IGoogleAuth:
    def create_register_url(self, redirect_url: str, access_type: str = 'offline') -> str:
        raise NotImplementedError

    def get_info_by_token(self, access_token: str) -> GoogleUserInfo | None:
        raise NotImplementedError

    def get_access_and_refresh_token(self, code: str, redirect_url: str) -> GoogleAccessRefreshToken:
        raise NotImplementedError

    def get_new_access_token(self, refresh_token: str) -> str:
        raise NotImplementedError