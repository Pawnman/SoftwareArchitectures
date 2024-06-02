from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, alias_generators, Field

from schemas.message import MessageSchema
from schemas.user import UserReadSchema

# Класс группового чата
class GroupChatSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, populate_by_name=True,
                              arbitrary_types_allowed=True)

    id: PydanticObjectId | None = Field(validation_alias='_id', default=None)
    members: list[UserReadSchema] | None = []
    messages: list[MessageSchema] | None = []
    group_name: str

