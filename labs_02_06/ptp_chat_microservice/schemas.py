from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict, alias_generators
import datetime


class UserReadSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, from_attributes=True, populate_by_name=True)
    id: int
    name: str | None = None
    last_name: str | None = None
    username: str
    is_active: bool | None = True

# Модель сообщения
class MessageSchema(BaseModel):
    text: str
    user: UserReadSchema
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


# Модель хранения PtP чата
class PtpChatSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, from_attributes=True, populate_by_name=True)

    id: PydanticObjectId | None = Field(validation_alias='_id', default=None)
    user_sender: UserReadSchema
    user_getter: UserReadSchema
    messages: list[MessageSchema] | None = []
