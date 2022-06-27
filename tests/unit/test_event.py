import json

from api.v1.servises import events
from api.v1.servises import authorization
from core.schemas.schemas import UserMessage, UserSchema, UserEvenSchema, UserEvent, DateEvent
from datetime import datetime


def test_online_user(test_app, monkeypatch):
    test_response = {"online user": [
                            {
                                "id": 2,
                                "email": "email2@email.ru"
                            },
                        ]
                    }

    async def mock_get_event_user_by_time(time: datetime):
        event_1 = UserEvent(id=1, type='Тип 1', owner=1)
        event_2 = UserEvent(id=2, type='Тип 2', owner=2)
        return [event_1, event_2]

    async def mock_get_user_by_id(user_id: int):
        return UserSchema(id=2, email='email2@email.ru')

    async def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    monkeypatch.setattr(events,
                        "get_event_user_by_time",
                        mock_get_event_user_by_time)

    monkeypatch.setattr(events,
                        "get_user_by_id",
                        mock_get_user_by_id)

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    response = test_app.get("event/online/",
                            headers={"Authorization": "Bearer email@email.ru"})

    assert response.status_code == 200
    assert response.json() == test_response


def test_long_polling(test_app, monkeypatch):
    test_time = datetime.utcnow()
    test_response = {'events': [{'id': 1, 'type': 'Тип 1'},
                                {'id': 2, 'type': 'Тип 2'}]}

    async def mock_get_subscribe_event_user_by_time(user_id: int, time: datetime):
        event_1 = DateEvent(id=1, type='Тип 1', owner=1, date=test_time)
        event_2 = DateEvent(id=2, type='Тип 2', owner=2, date=test_time)
        return [event_1, event_2]

    async def mock_get_user_by_id(user_id: int):
        return UserEvenSchema(id=2, email='email2@email.ru', last_event_date='2022-06-25 20:00:38.375')

    async def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    async def mock_set_user_last_event(user_id, last_event_date):
        return None
    monkeypatch.setattr(events,
                        "get_subscribe_event_user_by_time",
                        mock_get_subscribe_event_user_by_time)

    monkeypatch.setattr(events,
                        "get_user_by_id",
                        mock_get_user_by_id)

    monkeypatch.setattr(events,
                        "set_user_last_event",
                        mock_set_user_last_event)

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    response = test_app.get("event/polling/",
                            headers={"Authorization": "Bearer email@email.ru"})

    assert response.status_code == 200
    assert response.json() == test_response
