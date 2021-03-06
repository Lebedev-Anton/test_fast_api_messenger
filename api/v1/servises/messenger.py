from fastapi import HTTPException, status

from api.v1.servises.crud.crud import (get_user_by_email,
                                       get_sender_to_recipient_messages,
                                       set_user_message)
from core.schemas.schemas import UserSchema, UserMessage, UserMessages


async def get_user_email(email: str):
    """Запрос пользовательского email."""
    user = await get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь с {email} не существует'
        )
    return UserSchema(id=user.id, email=email)


async def get_messages_story(recipient: UserSchema,
                             sender: UserSchema) -> UserMessages:
    """Запрос сообщений от пользователя."""
    messages = await get_sender_to_recipient_messages(recipient.id, sender.id)
    messages_story = []
    for message in messages:
        messages_story.append(UserMessage(message=message.message))
    return UserMessages(messages=messages_story)


async def send_user_message(message: UserMessage,
                            recipient: UserSchema,
                            current_user: UserSchema) -> UserMessage:
    """Отправка сообщения от пользователю."""
    await set_user_message(message.message, recipient.id, current_user.id)
    return UserMessage(message=message.message)
