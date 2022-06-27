from typing import List
from core.schemas.schemas import UserSchema, EventSchema
from api.v1.servises.crud.crud import (set_event,
                                       set_event_subscriber,
                                       get_event_user_by_time,
                                       get_user_by_id,
                                       set_user_last_event,
                                       get_subscribe_event_user_by_time)

import asyncio
from datetime import datetime, timedelta


async def register_user_event(owner: UserSchema,
                              event: str,
                              subscribers: List[int]):
    """Регистрация события пользователя."""
    event = await set_event(owner.id, event)
    for subscriber in subscribers:
        await set_event_subscriber(event, subscriber)


async def get_online_user():
    """Запрос пользователей онлайн."""
    date = datetime.utcnow()
    d = date - timedelta(minutes=15)
    events = await get_event_user_by_time(d)
    users = []
    for event in events:
        user = await get_user_by_id(event.owner)
        online_user = UserSchema(id=user.id, email=user.email)
        if online_user not in users:
            users.append(UserSchema(id=user.id, email=user.email))
    return users


async def get_long_polling_event(user: UserSchema):
    """Реализация long polling."""
    user = await get_user_by_id(user.id)
    last_event_time = user.last_event_date
    if last_event_time is None:
        last_event_time = datetime.utcnow()
    for i in range(10):
        events = await get_subscribe_event_user_by_time(
            user.id, last_event_time)
        if len(events) != 0:
            last_event_time = events[0].date + timedelta(milliseconds=5)
            await set_user_last_event(user.id, last_event_time)
            return [EventSchema(id=event.id, type=event.type)
                    for event in events]
        await asyncio.sleep(2)
