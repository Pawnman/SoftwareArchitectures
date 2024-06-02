import httpx
from fastapi import APIRouter, Depends

from utils.handlers import handle_response
from routers.user_router import oauth2_scheme
from settings import settings

router = APIRouter(
    prefix="/group",
    tags=["group"],
)


@router.post("/create")
async def create_group(group_name: str, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.GROUP_CHAT_SERVICE_URL}/group_chat/create?group_name={group_name}",
                                     headers=headers)
        return handle_response(response)


@router.post("/new_member/{group_id}/{user_id}")
async def add_member_to_group(group_id: str, user_id: int, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.GROUP_CHAT_SERVICE_URL}/group_chat/add_member/{group_id}/{user_id}",
                                     headers=headers)
        return handle_response(response)


@router.post('/message/{group_id}')
async def send_message(message_text: str, group_id: str, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.GROUP_CHAT_SERVICE_URL}/group_chat/send_message/{group_id}?message_text={message_text}",
            headers=headers)
        return handle_response(response)


@router.get('/{group_id}')
async def get_group(group_id: str, token: str = Depends(oauth2_scheme)):

    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.GROUP_CHAT_SERVICE_URL}/group_chat/{group_id}",
            headers=headers)

        return handle_response(response)
