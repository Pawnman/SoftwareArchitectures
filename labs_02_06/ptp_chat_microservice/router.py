import httpx
from aiocircuitbreaker import circuit
from fastapi import APIRouter, Depends, HTTPException
from utils.jwt import oauth2_scheme, get_current_auth_user
from schemas import MessageSchema, PtpChatSchema, UserReadSchema
from settings import settings
from utils.utils import convert_ptp_chat_model_to_dict
from database.mongo_db import PtpChat

router = APIRouter(
    tags=["ptp_chat"],
    prefix="/ptp_chat",
)


@router.post('/send_message/{user_getter_id}', response_model=MessageSchema)
@circuit(failure_threshold=5, recovery_timeout=30)
async def send_message(message_text: str, user_getter_id: int, username: str = Depends(get_current_auth_user),
                       token: str = Depends(oauth2_scheme)):
    """
    Получаем на вход сообщение и отправляем его пользователю, сохраняем в базе данных и возвращаем сообщение

    """
    try:

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{settings.USER_SERVICE_URL}/user/?username={username}", headers=headers)
            user = response.json()

        message = MessageSchema(
            user=user,
            text=message_text
        )

        user = UserReadSchema.model_validate(user, from_attributes=True)
        ptp_chat = await PtpChat.find_one({'user_sender': user.model_dump()})

        if ptp_chat is None:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(f"{settings.USER_SERVICE_URL}/user/get/{user_getter_id}", headers=headers)
                user_getter = UserReadSchema.model_validate(response.json())

            ptp_chat = PtpChatSchema(
                user_sender=user,
                user_getter=user_getter
            )

            await PtpChat.insert_one(ptp_chat.model_dump(by_alias=False, exclude={'id'}))

            ptp_chat = await PtpChat.find_one({'user_sender': user.model_dump()})

        ptp_chat = PtpChatSchema.model_validate(ptp_chat, from_attributes=True)

        ptp_chat.messages.append(message)

        ptp_chat = await convert_ptp_chat_model_to_dict(ptp_chat)

        await PtpChat.update_one({'_id': ptp_chat.id}, {'$set': {'messages': ptp_chat.messages}})

        return message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/get_messages', response_model=list[PtpChatSchema])
@circuit(failure_threshold=5, recovery_timeout=30)
async def get_messages(username: str = Depends(get_current_auth_user), token: str = Depends(oauth2_scheme)):
    """
    Получаем все сообщения пользователя
    """

    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{settings.USER_SERVICE_URL}/user/?username={username}", headers=headers)
            user = UserReadSchema.model_validate(response.json())

        cursor = PtpChat.find(filter={'user_getter': user.model_dump()})

        ptp_chats_to_user = await cursor.to_list(length=None)

        return ptp_chats_to_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
