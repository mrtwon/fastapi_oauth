from typing import Protocol


class ITokenRepo(Protocol):
    def add_token(self, access_token: str, refresh_token: str) -> None:
        raise NotImplementedError

    def update_token(self, old_token: str, new_token: str) -> None:
        raise NotImplementedError

    def delete_token(self, token: str):
        raise NotImplementedError

    def get_refresh_token(self, access_token: str) -> str:
        raise NotImplementedError
