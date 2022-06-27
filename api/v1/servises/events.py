from typing import List
from core.schemas.schemas import UserSchema, EventSchema
from api.v1.servises.crud.crud import set_event, set_event_subscriber, get_event_user_by_time, get_user_by_id, set_user_last_event, get_subscribe_event_user_by_time

import time
from datetime import datetime, timedelta


async def register_user_event(owner: UserSchema, event: str, subscribers: List[int]):
    event = await set_event(owner.id, event)
    for subscriber in subscribers:
        set_event_subscriber(event.id, subscriber)


async def get_online_user():
    date = datetime.utcnow()
    d = date - timedelta(minutes=15)
    events = await get_event_user_by_time(d)
    users = []
    for event in events:
        user = get_user_by_id(event.owner)
        users.append(user)
    return users


def get_long_polling_event(user: UserSchema):
    user = get_user_by_id(user.id)
    last_event_time = user.last_event_date
    if last_event_time is None:
        last_event_time = datetime.utcnow()
    for i in range(3):
        events = get_subscribe_event_user_by_time(user.id, last_event_time)
        if len(events) != 0:
            last_event_time = events[0].date + timedelta(milliseconds=5)
            set_user_last_event(user.id, last_event_time)
            return [EventSchema(id=event.id, type=event.type) for event in events]
        time.sleep(2)
