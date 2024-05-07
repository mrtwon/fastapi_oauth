from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


from di.base import di_all
from infrastructure.table.table import map_user, map_session
from auth.base import di_all_oauth
from config import settings
from router.base import base_router

app = FastAPI()
di_all(app)
di_all_oauth(app, settings.__dict__)
map_user()
map_session()
origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
