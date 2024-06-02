import json

import httpx

from schemas.user_schemas import UserCreateSchema
from settings import settings
from fastapi import APIRouter

router = APIRouter(
    tags=["fixtures"],
    prefix="/fixtures"
)


@router.post("/add_users")
async def add_user_start_data():
    new_user = UserCreateSchema(username="first_begin_user", password="123qwe123", last_name="test",
                                name="testov")

    async with httpx.AsyncClient() as client:
        await client.post(f"{settings.USER_SERVICE_URL}/user/register",
                          content=json.dumps(new_user.model_dump(by_alias=True)))

    new_user2 = UserCreateSchema(username="second_begin_user", password="123qwe123", last_name="boy",
                                 name="golden")

    async with httpx.AsyncClient() as client:
        await client.post(f"{settings.USER_SERVICE_URL}/user/register",
                          content=json.dumps(new_user2.model_dump(by_alias=True)))
