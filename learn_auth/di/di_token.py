from fastapi import FastAPI

from infrastructure.repository.token.implementation import TokenRepo

from infrastructure.repository.token.interface import ITokenRepo


def get_token_repository():
    return TokenRepo()

def di_token(app: FastAPI):
    app.dependency_overrides[ITokenRepo] = get_token_repository