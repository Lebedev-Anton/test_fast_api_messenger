import json
from typing import List
import pytest
from api.v1.servises import groups
from api.v1.servises import authorization
from core.schemas.schemas import UserSchema, GroupSchema, Messages, UserMessage, Group, GroupUser


def test_show_group_message(test_app, monkeypatch):
    test_response = {
        'messages': [{'text': 'сообщение_1'}, {'text': 'сообщение_2'}]}

    async def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    async def mock_get_group_by_name_and_owner(name: str, owner_id: int):
        return Group(id=1, owner=1, name='group_1')

    async def mock_register_user_event(owner: UserSchema,
                                       event: str,
                                       subscribers: List[int]):
        return None

    async def mock_get_group_messages(group_id):
        message_1 = UserMessage(message='сообщение_1')
        message_2 = UserMessage(message='сообщение_2')
        return [message_1, message_2]

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    monkeypatch.setattr(groups,
                        "get_group_by_name_and_owner",
                        mock_get_group_by_name_and_owner)

    monkeypatch.setattr(groups,
                        "register_user_event",
                        mock_register_user_event)

    monkeypatch.setattr(groups,
                        "get_group_messages",
                        mock_get_group_messages)

    response = test_app.get("/group/group_1/",
                            headers={"Authorization": "Bearer email@email.ru"})

    assert response.status_code == 200
    assert response.json() == test_response


def test_post_group_message(test_app, monkeypatch):
    test_request = {"text": "тестовое сообщение", "group_id": 1}

    async def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    async def mock_get_group_by_group_id(group_id: int):
        group_1 = GroupUser(id=1, id_group=1, id_user=1)
        group_2 = GroupUser(id=2, id_group=1, id_user=2)
        return [group_1, group_2]

    async def mock_register_user_event(owner: UserSchema,
                                       event: str,
                                       subscribers: List[int]):
        return None

    async def mock_set_group_message(user_message: str,
                                     group_id: int,
                                     user_id: int):
        return None

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    monkeypatch.setattr(groups,
                        "get_group_by_group_id",
                        mock_get_group_by_group_id)

    monkeypatch.setattr(groups,
                        "register_user_event",
                        mock_register_user_event)

    monkeypatch.setattr(groups,
                        "set_group_message",
                        mock_set_group_message)

    response = test_app.post("/group/group_1/",
                            headers={"Authorization": "Bearer email@email.ru"},
                            data=json.dumps(test_request),)

    assert response.status_code == 201
    assert response.json() == test_request


def test_user_group(test_app, monkeypatch):
    test_request = {"groups": [
                            {
                                "id": 1,
                                "owner": 1,
                                "name": "группа 1"
                            },
                            {
                                "id": 2,
                                "owner": 2,
                                "name": "группа 2"
                            },
                        ]
                    }

    async def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    async def mock_get_user_groups(user_id: int):
        group_1 = Group(id=1, owner=1, name='группа 1')
        group_2 = Group(id=2, owner=2, name='группа 2')
        return [group_1, group_2]

    async def mock_register_user_event(owner: UserSchema,
                                       event: str,
                                       subscribers: List[int]):
        return None

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    monkeypatch.setattr(groups,
                        "get_user_groups",
                        mock_get_user_groups)

    monkeypatch.setattr(groups,
                        "register_user_event",
                        mock_register_user_event)

    response = test_app.get("/group/show/me/",
                            headers={"Authorization": "Bearer email@email.ru"})

    assert response.status_code == 200
    assert response.json() == test_request