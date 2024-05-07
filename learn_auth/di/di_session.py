from fastapi import Depends, FastAPI

from di.di_setup import Session
from infrastructure.repository.session.implementation import SessionRepo
from infrastructure.repository.session.interface import ISessionRepo


def get_session(session: Session = Depends()):
    return SessionRepo(session)


def di_session(app: FastAPI):
    app.dependency_overrides[ISessionRepo] = get_session
