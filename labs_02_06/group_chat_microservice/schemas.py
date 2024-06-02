import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, alias_generators, Field


class UserReadSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, from_attributes=True, populate_by_name=True)
    id: int
    name: str | None = None
    last_name: str | None = None
    username: str
    is_active: bool | None = True


class MessageSchema(BaseModel):
    text: str
    user: UserReadSchema
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class GroupChatSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, populate_by_name=True,
                              arbitrary_types_allowed=True)

    id: PydanticObjectId | None = Field(validation_alias='_id', default=None)
    members: list[UserReadSchema] | None = []
    messages: list[MessageSchema] | None = []
    group_name: str
