import json
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.handlers import handle_response
from schemas.user import UserCreateSchema, UserUpdateSchema
from settings import settings

router = APIRouter(
    tags=['user'],
    prefix="/user",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    form_data_dict = form_data.__dict__

    data = {
        "grant_type": form_data_dict.get("grant_type"),
        "username": form_data_dict.get("username"),
        "password": form_data_dict.get("password"),
        "scope": form_data_dict.get("scope"),
        "client_id": form_data_dict.get("client_id"),
        "client_secret": form_data_dict.get("client_secret"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.USER_SERVICE_URL}/user/token", data=data)
        return handle_response(response)


@router.post('/refresh')
async def refresh_token(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.USER_SERVICE_URL}/user/refresh", headers=headers)
        return handle_response(response)


@router.post('/logout')
async def logout(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.USER_SERVICE_URL}/user/logout", headers=headers)
        return handle_response(response)


@router.post('/register')
async def create_new_user(new_user: UserCreateSchema):
    data = new_user.model_dump(by_alias=True)

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.USER_SERVICE_URL}/user/register", content=json.dumps(data))
        return handle_response(response)


@router.get('/me', status_code=status.HTTP_200_OK)
async def get_me(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_SERVICE_URL}/user/me", headers=headers)
        return handle_response(response)


@router.patch('/me', status_code=status.HTTP_202_ACCEPTED)
async def update_me(new_data: UserUpdateSchema, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    data = new_data.model_dump(by_alias=True)

    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{settings.USER_SERVICE_URL}/user/me", headers=headers,
                                      content=json.dumps(data))
        return handle_response(response)


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{settings.USER_SERVICE_URL}/user/me", headers=headers)
        return handle_response(response)


@router.get('/search/{mask}')
async def get_user_by_mask(mask: str, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_SERVICE_URL}/user/search/{mask}", headers=headers)
        return handle_response(response)


@router.get('/')
async def get_user_by_username(username: str, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_SERVICE_URL}/user/?username={username}", headers=headers)
        return handle_response(response)


@router.get('/get/{user_id}')
async def search_user(user_id: int, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_SERVICE_URL}/user/get/{user_id}", headers=headers)
        return handle_response(response)
