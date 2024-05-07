import requests
from auth.google.interface import IGoogleAuth
from auth.google.model import GoogleUserInfo
from auth.google.model import GoogleAccessRefreshToken
from base.exception import ErrorInProcessAuthException


class GoogleAuth(IGoogleAuth):
    OAUTH_REGISTER_URL = 'https://accounts.google.com/o/oauth2/v2/auth'

    def __init__(self, client_id: str, secret: str):
        self.google_client_id = client_id
        self.google_secret = secret

    def create_register_url(self, redirect_url: str, access_type: str = 'offline'):
        return self.OAUTH_REGISTER_URL + f'?client_id={self.google_client_id}&redirect_uri={redirect_url}&access_type={access_type}&response_type=code&scope=openid'

    def get_info_by_token(self, access_token: str) -> GoogleUserInfo | None:
        r = requests.get(f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}')
        if r.status_code != 200:
            return None
        try:
            dict_result = r.json()
        except:
            raise ErrorInProcessAuthException()
        return GoogleUserInfo.model_validate(dict_result)

    def get_access_and_refresh_token(self, code: str, redirect_url: str) -> GoogleAccessRefreshToken | None:
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        r = requests.post('https://www.googleapis.com/oauth2/v4/token', headers=headers, data={
            'code': code,
            'client_id': self.google_client_id,
            'client_secret': self.google_secret,
            'redirect_uri': redirect_url,
            'grant_type': 'authorization_code'
        })
        if r.status_code != 200:
            raise ErrorInProcessAuthException()
        result_dict = r.json()
        return GoogleAccessRefreshToken.model_validate(result_dict)

    def get_new_access_token(self, refresh_token) -> str:
        r = requests.post(
            'https://www.googleapis.com/oauth2/v4/token',
            headers={'Content-type': 'application/x-www-form-urlencoded'},
            data={
                'client_secret': self.google_secret,
                'client_id': self.google_client_id,
                'refresh_token': refresh_token,
                'grant_type': "refresh_token"
            })
        if r.status_code != 200:
            raise ErrorInProcessAuthException()
        try:
            return r.json()['access_token']
        except:
            raise ErrorInProcessAuthException()
