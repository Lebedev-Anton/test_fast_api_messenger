from fastapi import HTTPException, status

from api.v1.servises.crud.crud import get_user_by_email, get_sender_to_recipient_messages, set_user_message
from api.v1.servises.events import register_user_event
from core.schemas.schemas import UserSchema, MessageSchema


def get_user_email(email: str):
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь с {email} не существует'
        )
    return user


def get_messages_story(recipient: UserSchema, sender: UserSchema):
    register_user_event(sender, 'message_story', [])
    result = get_sender_to_recipient_messages(recipient.id, sender.id)
    return result


def send_user_message(message: MessageSchema,
                      recipient: UserSchema,
                      current_user: UserSchema) -> MessageSchema:
    new_message = set_user_message(message.text, recipient.id, current_user.id)
    register_user_event(current_user, 'send_message', [recipient.id])
    return MessageSchema(text=new_message.message)
