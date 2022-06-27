from typing import List
from core.models import user, message, group, group_users, event, event_subscriber
from core.models import db_session
from datetime import datetime
from core.models import database


async def get_user_by_email(email: str) -> user:
    query = user.select().where(email == user.c.email)
    return await database.fetch_one(query=query)


async def get_user_by_id(user_id: int) -> user:
    query = user.select().where(user_id == user.c.id)
    return await database.fetch_one(query=query)


async def get_sender_to_recipient_messages(recipient_id: int,
                                           sender_id: int) -> message:
    query = message.select().where(sender_id == message.c.sender,
                                   recipient_id == message.c.recipient,
                                   False == message.c.is_group,
                                   )
    return await database.fetch_all(query=query)


async def set_new_user(email: str) -> user:
    query = user.insert().values(email=email)
    return await database.execute(query=query)


async def set_user_message(message_user: str,
                           recipient_id: int,
                           sender_id: int) -> message:
    query = message.insert().values(message=message_user,
                                    sender=sender_id,
                                    recipient=recipient_id,
                                    is_group=False,
                                    )
    return await database.execute(query=query)


async def set_new_group(owner_id: int, name: str, users_id: List[int]):
    query = group.insert().values(owner=owner_id, name=name)
    new_group = await database.execute(query=query)

    for user_id in users_id:
        query = group_users.insert().values(id_group=new_group, id_user=user_id)
        await database.execute(query=query)


async def get_group_by_name_and_owner(name: str, owner_id: int):
    query = group.select().where(name == group.c.name, owner_id == group.c.owner)
    return await database.fetch_one(query=query)


async def get_group_messages(group_id: int):
    query = message.select().where(group_id == message.c.group)
    return await database.fetch_all(query=query)


async def set_group_message(user_message: str, group_id: int, user_id: int):
    query = message.insert().values(message=user_message,
                                    sender=user_id,
                                    is_group=True,
                                    group=group_id,
                                    )
    return await database.execute(query=query)


async def get_user_groups(user_id: int):
    query = group_users.select().where(user_id == group_users.c.id_user)
    groups_id = await database.fetch_all(query=query)
    groups = []
    for group_id in groups_id:
        query = group.select().where(group_id.id_group == group.c.id)
        user_group = await database.fetch_one(query=query)
        groups.append(user_group)
    return groups


async def set_event(owner_id: int, event_type: str):
    query = event.insert().values(owner=owner_id,
                                  type=event_type)
    return await database.execute(query=query)


def set_event_subscriber(event_id: int, subscriber_id: int):
    event_subscriber = event_subscriber(id_event=event_id, id_user=subscriber_id)
    db_session.add(event_subscriber)
    db_session.commit()
    return event_subscriber


async def get_group_by_group_id(group_id: int):
    query = group_users.select().where(group_id == group_users.c.id_group)
    return await database.fetch_all(query=query)


async def get_event_user_by_time(time: datetime):
    events = await event.query.filter(event.date > time).order_by(
        event.date.desc()
    ).all()
    return events


def set_user_last_event(user_id, last_event_date):
    user = user.query.filter_by(id=user_id).first()
    user.last_event_date = last_event_date
    db_session.commit()
    return user


def get_subscribe_event_user_by_time(user_id: int, time: datetime):
    events = event_subscriber.query.filter(
        event_subscriber.id_user == user_id
    ).order_by(
        event_subscriber.date.desc()
    ).all()
    user_events = []
    for event in events:
        user_event = event.query.filter_by(id=event.id_event).first()
        if user_event.date > time:
            user_events.append(user_event)
    return user_events
