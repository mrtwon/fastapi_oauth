from fastapi import APIRouter
from .auth_google import router as auth_google
from .auth_basic import router as auth_basic
from .auth_action import router as auth_profile
from .auth_vk import router as auth_vk
from .auth_google import router as auth_google
base_router = APIRouter()

base_router.include_router(auth_basic, prefix='/auth/basic')
base_router.include_router(auth_vk, prefix='/auth/vk')
base_router.include_router(auth_google, prefix='/auth/google')
base_router.include_router(auth_profile, prefix='/auth_action')
