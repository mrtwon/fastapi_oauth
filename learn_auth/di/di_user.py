from fastapi import FastAPI, Depends

from di.di_setup import Session
from infrastructure.repository.user.implementation import UserRepo
from infrastructure.repository.user.interface import IUserRepo


def get_user_repository(session: Session = Depends()):
    return UserRepo(session)


def di_user(app: FastAPI):
    app.dependency_overrides[IUserRepo] = get_user_repository
