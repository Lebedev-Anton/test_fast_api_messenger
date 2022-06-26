# import json
# import pytest
# from api.v1.servises import groups
# from api.v1.servises import authorization
# from core.schemas.schemas import UserSchema, GroupSchema, Messages
#
#
# def test_show_group_message(test_app, monkeypatch):
#     test_response_payload = {"group_messages": []}
#
#     def mock_get_user_by_email(email: str):
#         return UserSchema(id=1, email='email@email.ru')
#
#     def mock_get_group_by_name_and_owner(name: str, owner_id: int):
#         return GroupSchema(id=1, owner=1, name='group_1')
#
#     def mock_get_group_messages(group_id):
#         return Messages(messages=[])
#
#     monkeypatch.setattr(authorization,
#                         "get_user_by_email",
#                         mock_get_user_by_email)
#
#     monkeypatch.setattr(groups,
#                         "get_group_by_name_and_owner",
#                         mock_get_group_by_name_and_owner)
#
#     monkeypatch.setattr(groups,
#                         "get_group_messages",
#                         mock_get_group_messages)
#
#     response = test_app.get("/group/group_1/",
#                             headers={"Authorization": "Bearer email@email.ru"})
#
#     assert response.status_code == 200
#     assert response.json() == test_response_payload