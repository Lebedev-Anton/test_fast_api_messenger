from fastapi import APIRouter, Depends

from api.v1.servises.messenger import (get_user_email,
                                       get_messages_story,
                                       send_user_message)
from api.v1.servises.authorization import get_current_user
from core.schemas.schemas import UserSchema, UserMessage, UserMessages

router = APIRouter()


@router.get("/user/{email}", response_model=UserMessages)
async def show_user_message(
        recipient: UserSchema = Depends(get_user_email),
        current_user: UserSchema = Depends(get_current_user)):
    """Запрос сообщений от пользователя."""
    messages = await get_messages_story(recipient, current_user)
    return messages


@router.post("/user/{email}", response_model=UserMessage, status_code=201)
async def post_user_message(
        message: UserMessage,
        recipient: UserSchema = Depends(get_user_email),
        current_user: UserSchema = Depends(get_current_user),):
    """Отправка сообщений пользователю."""
    new_message = await send_user_message(message, recipient, current_user)
    return new_message
