from fastapi import Depends, HTTPException, status
from core.schemas.schemas import RegistrationSchema, UserSchema, GroupSchema, MessageGroupSchema, MessageSchema, Messages, Group
from api.v1.servises.crud.crud import get_user_by_id, set_new_group, get_group_by_name_and_owner, get_group_messages, set_group_message, get_user_groups, \
    get_group_by_group_id

from api.v1.servises.events import register_user_event


async def get_group_info(group_info: GroupSchema):
    owner_user = await get_user_by_id(group_info.owner)
    if owner_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь с id = {group_info.owner} не существует'
        )
    for user_id in group_info.users:
        user_in_group = await get_user_by_id(user_id)
        if user_in_group is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователь с id = {user_id} не существует'
            )
    return group_info


async def get_group_story(group_name: str, owner: UserSchema) -> Messages:
    group = await get_group_by_name_and_owner(group_name, owner.id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Группа {group_name} не существует'
        )
    await register_user_event(owner, 'message_story', [])
    messages = await get_group_messages(group.id)
    messages_schema = []
    for message in messages:
        message_schema = MessageSchema(text=message.message)
        messages_schema.append(message_schema)

    return Messages(messages=messages_schema)


async def send_group_message(message: MessageGroupSchema,
                             current_user: UserSchema) -> MessageGroupSchema:
    group_id = message.group_id
    await set_group_message(message.text, group_id, current_user.id)
    groups = await get_group_by_group_id(group_id)
    await register_user_event(current_user, 'group_message',
                        [group.id_user for group in groups])
    return MessageGroupSchema(text=message.text, group_id=message.group_id)


async def register_new_group(group_info: GroupSchema):
    await set_new_group(group_info.owner, group_info.name, group_info.users)
    owner = UserSchema(id=group_info.owner, email='')
    await register_user_event(owner, 'register_group', group_info.users)
    return group_info


async def get_group_by_user(current_user: UserSchema):
    await register_user_event(current_user, 'group_by_user', [])
    groups = await get_user_groups(current_user.id)
    user_groups = []
    for group in groups:
        user_groups.append(Group(id=group.id, owner=group.owner, name=group.name))
    return {'groups': user_groups}
