from fastapi import APIRouter

from database.mongo_db import GroupChat
from schemas import MessageSchema, GroupChatSchema

router = APIRouter(
    prefix="/fixtures",
    tags=["fixtures"],
)


@router.post('/add_group_chat')
async def add_group_chat_fixture():
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

    group = GroupChatSchema(
        members=[user1, user2],
        messages=[message1, message2],
        group_name="test_group"

    )

    await GroupChat.insert_one(group.model_dump(by_alias=False, exclude={'id'}))
