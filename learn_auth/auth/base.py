from fastapi import FastAPI

from auth.google.google_auth import GoogleAuth
from auth.google.interface import IGoogleAuth
from auth.vk.interface import IVKAuth
from auth.vk.vk_auth import VKAuth


def get_vk_auth(env: dict):
    return VKAuth(env['VK_APP_ID'], env['VK_SERVICE_KEY'])


def get_google_auth(env: dict):
    return GoogleAuth(env['GOOGLE_CLIENT_ID'], env['GOOGLE_SECRET'])


def di_all_oauth(app: FastAPI, env: dict):
    app.dependency_overrides[IVKAuth] = lambda : get_vk_auth(env)
    app.dependency_overrides[IGoogleAuth] = lambda : get_google_auth(env)
