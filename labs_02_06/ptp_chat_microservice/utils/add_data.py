from fastapi import APIRouter

from database.mongo_db import PtpChat
from schemas import MessageSchema, PtpChatSchema

router = APIRouter(
    tags=["fixtures"],
    prefix="/fixtures"
)


@router.post("/add_ptp_chat")
async def add_ptp_chat_fixtures():
    user1 = {
        "id": 1,
        'username': 'test_user',
        'last_name': 'test_last_name',
        'name': 'test_first_name',
        'is_active': True
    }

    user2 = {
        "id": 2,
        'username': 'test_user2',
        'last_name': 'test_last_name2',
        'name': 'test_first_name2',
        'is_active': True
    }

    message1 = MessageSchema(
        text='text',
        user=user1
    )

    message2 = MessageSchema(
        text='text2',
        user=user2
    )

    ptp_chat = PtpChatSchema(
        user_sender=user1,
        user_getter=user2,
        messages=[message1, message2]
    )

    await PtpChat.insert_one(ptp_chat.model_dump(by_alias=False, exclude={'id'}))
