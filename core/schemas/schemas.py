from typing import List
from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    email: str


class UserSchema(BaseModel):
    id: int
    email: str


class MessageSchema(BaseModel):
    text: str


class MessageGroupSchema(MessageSchema):
    group_id: int


class GroupSchema(BaseModel):
    owner: int
    name: str
    users: List[int]


class EventSchema(BaseModel):
    id: int
    type: str
