import httpx
from fastapi import APIRouter, HTTPException

from settings import settings

router = APIRouter(
    tags=['begin_data'],
    prefix='/begin_data'
)


@router.post('/')
async def add_begin_data():

    try:

        await add_user_begin_data()
        await add_group_ptp_begin_data()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_user_begin_data():
    async with httpx.AsyncClient() as client:
        await client.post(f"{settings.USER_SERVICE_URL}/fixtures/add_users")


async def add_group_ptp_begin_data():
    async with httpx.AsyncClient() as client:
        await client.post(f"{settings.PTP_CHAT_SERVICE_URL}/fixtures/add_ptp_chat")

    async with httpx.AsyncClient() as client:
        await client.post(f"{settings.GROUP_CHAT_SERVICE_URL}/fixtures/add_group_chat")
