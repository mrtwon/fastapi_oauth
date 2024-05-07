from fastapi import HTTPException
from starlette import status


class BException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidEmailPasswordException(BException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "invalid email or password"


class UserAlreadyExist(BException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "user already exist"


class UserNotFoundException(BException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "user not found"


class SessionNotFoundException(BException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "session not found"


class NotAuthException(BException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "you not auth"


class SessionAlreadyFinish(BException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'session is finish'


class ErrorInProcessAuthException(BException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "error in process auth"
