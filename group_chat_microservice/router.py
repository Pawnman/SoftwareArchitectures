import httpx
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from utils.jwt import get_current_auth_user, oauth2_scheme
from database.mongo_db import GroupChat
from schemas import GroupChatSchema, MessageSchema, UserReadSchema
from settings import settings
from utils.utils import convert_group_model_to_dict


router = APIRouter(
    tags=["group_chat"],
    prefix="/group_chat",
)


@router.post("/create", response_model=GroupChatSchema)
async def create_group(group_name: str, username: str = Depends(get_current_auth_user),
                       token: str = Depends(oauth2_scheme)):

    try:

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{settings.USER_SERVICE_URL}/user/?username={username}", headers=headers)
            user = response.json()

        group_chat = GroupChatSchema(group_name=group_name, members=[user])
        new_group = await GroupChat.insert_one(group_chat.model_dump(by_alias=False, exclude={'id'}))

        group = await GroupChat.find_one({"_id": new_group.inserted_id})

        return group

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_member/{group_id}/{user_id}", response_model=GroupChatSchema)
async def add_member_to_group(group_id: str, user_id: int, token: str = Depends(oauth2_scheme)):

    try:

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{settings.USER_SERVICE_URL}/user/get/{user_id}", headers=headers)
            user = UserReadSchema.model_validate(response.json())

        group = GroupChatSchema.model_validate(await GroupChat.find_one({"_id": ObjectId(group_id)}),
                                               from_attributes=True)

        if user not in group.members:
            group.members.append(user)

        group = await convert_group_model_to_dict(group)

        await GroupChat.update_one({'_id': ObjectId(group.id)},
                                   {'$set': {'members': group.members}})

        upd_group = await GroupChat.find_one({"_id": ObjectId(group_id)})

        return upd_group

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/send_message/{group_id}', response_model=MessageSchema)
async def send_message(message_text: str, group_id: str, username: str = Depends(get_current_auth_user),
                       token: str = Depends(oauth2_scheme)):

    try:

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{settings.USER_SERVICE_URL}/user/?username={username}", headers=headers)
            user = response.json()

        message = MessageSchema(text=message_text, user=user)
        group = GroupChatSchema.model_validate(await GroupChat.find_one({"_id": ObjectId(group_id)}),
                                               from_attributes=True)
        group.messages.append(message)
        group = await convert_group_model_to_dict(group)

        await GroupChat.update_one({'_id': ObjectId(group.id)},
                                   {'$set': {'messages': group.messages}})

        return message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{group_id}', dependencies=[Depends(get_current_auth_user)], response_model=GroupChatSchema)
async def get_group(group_id: str):

    try:
        group = await GroupChat.find_one({'_id': ObjectId(group_id)})

        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        return group

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
