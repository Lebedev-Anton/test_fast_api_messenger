import json
from typing import List

from api.v1.servises import authorization
from core.schemas.schemas import UserSchema
from api.v1.servises import groups


def test_register_user(test_app, monkeypatch):
    test_request = {"email": "test_user@mail.ru"}
    test_response = {"email": "test_user@mail.ru", "id": 2}

    async def mock_set_new_user(email: str):
        return 2

    async def mock_get_user_by_email(email: str):
        return None

    monkeypatch.setattr(authorization,
                        "set_new_user",
                        mock_set_new_user)

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    response = test_app.post("/registration/user/",
                             data=json.dumps(test_request), )

    assert response.status_code == 201
    assert response.json() == test_response


def test_register_group(test_app, monkeypatch):
    test_response = {"owner": 1, "name": "group_1", "users": [1, 2, 3]}

    async def mock_set_new_group(owner_id: int,
                                 name: str,
                                 users_id: List[int]):
        return None

    async def mock_register_user_event(owner: UserSchema,
                                       event: str,
                                       subscribers: List[int]):
        return None

    async def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    monkeypatch.setattr(groups,
                        "set_new_group",
                        mock_set_new_group)

    monkeypatch.setattr(groups,
                        "register_user_event",
                        mock_register_user_event)

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    response = test_app.post("/registration/group/",
                             headers={"Authorization": "Bearer email@email.ru"},
                             data=json.dumps(test_response),)

    assert response.status_code == 201
    assert response.json() == test_response
