import json

from api.v1.servises import messenger
from api.v1.servises import authorization
from core.schemas.schemas import UserMessage, UserSchema


def test_show_user_message(test_app, monkeypatch):
    test_response = {
        'messages': [{'message': 'сообщение_1'}, {'message': 'сообщение_2'}]}

    async def mock_get_sender_to_recipient_messages(recipient_id: int,
                                              sender_id: int):
        message_1 = UserMessage(message='сообщение_1')
        message_2 = UserMessage(message='сообщение_2')
        return [message_1, message_2]

    def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    monkeypatch.setattr(messenger,
                        "get_sender_to_recipient_messages",
                        mock_get_sender_to_recipient_messages)

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    response = test_app.get("/message/user/email3@mail.ru",
                            headers={"Authorization": "Bearer email@email.ru"})

    assert response.status_code == 200
    assert response.json() == test_response


def test_post_user_message(test_app, monkeypatch):
    test_response = {"message": "Тестовое сообщение"}

    async def mock_set_user_message(message_user: str,
                                    recipient_id: int,
                                    sender_id: int):
        return UserMessage(message='Тестовое сообщение')

    def mock_get_user_by_email(email: str):
        return UserSchema(id=1, email='email@email.ru')

    monkeypatch.setattr(messenger,
                        "set_user_message",
                        mock_set_user_message)

    monkeypatch.setattr(authorization,
                        "get_user_by_email",
                        mock_get_user_by_email)

    response = test_app.post("/message/user/email3@mail.ru",
                             headers={"Authorization": "Bearer email@email.ru"},
                             data=json.dumps(test_response),)

    assert response.status_code == 201
    assert response.json() == test_response
