import requests
from auth.vk.interface import IVKAuth
from base.exception import ErrorInProcessAuthException


class VKAuth(IVKAuth):
    def __init__(self, app_id: str, secret_key: str):
        self.app_id = app_id
        self.service_key = secret_key

    def create_register_url(self, redirect_url: str) -> str:
        return f'https://id.vk.com/auth?uuid=$gggfggg&app_id={self.app_id}&response_type=silent_token&redirect_uri={redirect_url}&redirect_state=gfdggf'

    def get_user_id_by_silent_token(self, silent_token: str) -> str:
        r = requests.post('https://api.vk.com/method/auth.exchangeSilentAuthToken', data={
            'v': '5.131',
            'token': silent_token,
            'access_token': self.service_key,
            'uuid': '$gggfggg'
        })
        if r.status_code != 200:
            raise ErrorInProcessAuthException()
        result_json = r.json()
        try:
            return result_json['response']['user_id']
        except:
            raise ErrorInProcessAuthException()