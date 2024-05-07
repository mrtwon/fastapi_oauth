from base.schema import BaseSchema


class GoogleUserInfo(BaseSchema):
    sub: str
    picture: str


class GoogleAccessRefreshToken(BaseSchema):
    access_token: str
    refresh_token: str
