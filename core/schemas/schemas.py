from typing import List
from pydantic import BaseModel
from datetime import datetime


class RegistrationSchema(BaseModel):
    email: str


class UserSchema(BaseModel):
    id: int
    email: str


class MessageSchema(BaseModel):
    text: str


class UserMessage(BaseModel):
    message: str


class UserMessages(BaseModel):
    messages: List[UserMessage]


class Messages(BaseModel):
    messages: List[MessageSchema]


class MessageGroupSchema(MessageSchema):
    group_id: int


class GroupSchema(BaseModel):
    owner: int
    name: str
    users: List[int]


class EventSchema(BaseModel):
    id: int
    type: str
