from fastapi import Depends, HTTPException, status
from core.schemas.schemas import RegistrationSchema, UserSchema, GroupSchema, MessageGroupSchema
from api.v1.servises.crud.crud import get_user_by_id, set_new_group, get_group_by_name_and_owner, get_group_messages, set_group_message, get_user_groups, \
    get_group_by_group_id

from api.v1.servises.events import register_user_event


def get_group_info(group_info: GroupSchema):
    owner_user = get_user_by_id(group_info.owner)
    if owner_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь с id = {group_info.owner} не существует'
        )
    for user_id in group_info.users:
        user_in_group = get_user_by_id(user_id)
        if user_in_group is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователь с id = {user_id} не существует'
            )
    return group_info


def get_group_story(group_name: str, owner: UserSchema):
    group = get_group_by_name_and_owner(group_name, owner.id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Группа {group_name} не существует'
        )
    register_user_event(owner, 'message_story', [])
    messages = get_group_messages(group.id)
    return messages


def send_group_message(message: MessageGroupSchema,
                       current_user: UserSchema) -> MessageGroupSchema:
    group_id = message.group_id
    message = set_group_message(message.text, group_id, current_user.id)
    groups = get_group_by_group_id(group_id)
    register_user_event(current_user, 'group_message',
                        [group.id_user for group in groups])
    return MessageGroupSchema(text=message.message, group_id=message.group)


def register_new_group(group_info: GroupSchema):
    set_new_group(group_info.owner, group_info.name, group_info.users)
    owner = UserSchema(id=group_info.owner, email='')
    register_user_event(owner, 'register_group', group_info.users)
    return group_info


def get_group_by_user(current_user: UserSchema):
    register_user_event(current_user, 'group_by_user', [])
    groups = get_user_groups(current_user.id)
    return groups
