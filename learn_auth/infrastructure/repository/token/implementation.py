import redis

from infrastructure.repository.token.interface import ITokenRepo


class TokenRepo(ITokenRepo):
    def add_token(self, access_token: str, refresh_token: str) -> None:
        client = redis.Redis()
        client.set(access_token, refresh_token)

    def delete_token(self, token: str) -> None:
        client = redis.Redis()
        client.delete(token)

    def get_refresh_token(self, access_token: str) -> str | None:
        client = redis.Redis()
        return client.get(access_token)

    def update_token(self, old_token: str, new_token: str) -> None:
        client = redis.Redis()
        client.rename(old_token, new_token)