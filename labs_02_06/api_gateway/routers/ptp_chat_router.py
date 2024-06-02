import httpx
from fastapi import APIRouter, Depends

from utils.handlers import handle_response
from routers.user_router import oauth2_scheme
from settings import settings
from aiocircuitbreaker import circuit

router = APIRouter(
    tags=["ptp"],
    prefix="/ptp",
)


@router.post('/message/{user_id}')
@circuit(failure_threshold=5, recovery_timeout=30)
async def send_message(message_text: str, user_id: int,
                       token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(
            f"{settings.PTP_CHAT_SERVICE_URL}/ptp_chat/send_message/{user_id}?message_text={message_text}",
            headers=headers)
        return handle_response(response)


@router.get('/messages')
@circuit(failure_threshold=5, recovery_timeout=30)
async def get_messages(token: str = Depends(oauth2_scheme)):

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(
            f"{settings.PTP_CHAT_SERVICE_URL}/ptp_chat/get_messages",
            headers=headers)
        return handle_response(response)
