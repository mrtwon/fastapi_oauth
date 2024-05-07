from fastapi import FastAPI
from di.di_token import di_token
from di.di_user import di_user
from di.di_setup import di_setup
from di.di_session import di_session



def di_all(app: FastAPI):
    di_setup(app)
    di_user(app)
    di_token(app)
    di_session(app)
