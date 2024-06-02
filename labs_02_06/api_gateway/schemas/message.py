import datetime
from pydantic import BaseModel, Field
from schemas.user import UserReadSchema

# Модель класс сообщения
class MessageSchema(BaseModel):
    text: str
    user: UserReadSchema
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
