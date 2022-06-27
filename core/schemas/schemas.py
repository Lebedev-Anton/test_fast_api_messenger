from typing import List
from pydantic import BaseModel
from datetime import datetime


class RegistrationSchema(BaseModel):
    email: str


class UserSchema(BaseModel):
    id: int
    email: str


class UserEvenSchema(UserSchema):
    last_event_date: datetime


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


class Group(BaseModel):
    id: int
    owner: int
    name: str


class GroupUser(BaseModel):
    id: int
    id_group: int
    id_user: int


class EventSchema(BaseModel):
    id: int
    type: str


class UserEvent(EventSchema):
    owner: int


class DateEvent(UserEvent):
    date: datetime

