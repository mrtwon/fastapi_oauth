class IVKAuth:
    def create_register_url(self, redirect_url: str) -> str:
        raise NotImplementedError

    async def get_user_id_by_silent_token(self, silent_token: str) -> str:
        raise NotImplementedError
