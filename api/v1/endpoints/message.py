from fastapi import APIRouter, Depends

from api.v1.servises.messenger import (get_user_email,
                                       get_messages_story,
                                       send_user_message)
from api.v1.servises.authorization import get_current_user
from core.schemas.schemas import UserSchema, MessageSchema

router = APIRouter()


@router.get("/user/{email}")
async def show_user_message(recipient: UserSchema = Depends(get_user_email),
                     current_user: UserSchema = Depends(get_current_user)):
    messages = get_messages_story(recipient, current_user)
    return {"messages": messages}


@router.post("/user/{email}", response_model=MessageSchema, status_code=201)
async def post_user_message(
        message: MessageSchema,
        recipient: UserSchema = Depends(get_user_email),
        current_user: UserSchema = Depends(get_current_user),):
    new_message = send_user_message(message, recipient, current_user)
    return new_message
