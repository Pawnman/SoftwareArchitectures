from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from schemas.message import MessageSchema
from schemas.user import UserReadSchema

# Модель класс чата PtP
class PtpChatSchema(BaseModel):
    id: PydanticObjectId | None = Field(validation_alias='_id', default=None)
    user_sender: UserReadSchema
    user_getter: UserReadSchema
    messages: list[MessageSchema] | None = []
