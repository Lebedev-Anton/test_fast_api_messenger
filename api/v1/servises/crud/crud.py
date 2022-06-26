from typing import List
from core.models import User, message, group, GroupUsers, Event, EventSubscriber
from core.models import db_session
from datetime import datetime
from core.models import database


def get_user_by_email(email: str) -> User:
    user = User.query.filter_by(email=email).first()
    return user


def get_user_by_id(user_id: int) -> User:
    user = User.query.filter_by(id=user_id).first()
    return user


async def get_sender_to_recipient_messages(recipient_id: int,
                                           sender_id: int) -> message:
    query = message.select().where(sender_id == message.c.sender,
                                   recipient_id == message.c.recipient,
                                   False == message.c.is_group,
                                   )
    return await database.fetch_all(query=query)


def set_new_user(email: str) -> User:
    new_user = User(email=email)
    db_session.add(new_user)
    db_session.commit()
    return new_user


async def set_user_message(message_user: str,
                           recipient_id: int,
                           sender_id: int) -> message:
    query = message.insert().values(message=message_user,
                                    sender=sender_id,
                                    recipient=recipient_id,
                                    is_group=False,
                                    )
    return await database.execute(query=query)


def set_new_group(owner_id: int, name: str, users_id: List[int]):
    new_group = group(owner=owner_id, name=name)
    db_session.add(new_group)
    db_session.commit()

    for user_id in users_id:
        group_user = GroupUsers(id_group=new_group.id, id_user=user_id)
        db_session.add(group_user)
    db_session.commit()


async def get_group_by_name_and_owner(name: str, owner_id: int):
    query = group.select().where(name == group.c.name, owner_id == group.c.owner)
    return await database.fetch_all(query=query)


def get_group_messages(group_id: int):
    messages = message.query.filter_by(group=group_id).all()
    return messages


def set_group_message(message: str, group_id: int, user_id: int):
    message = message(message=message, sender=user_id,
                      is_group=True, group=group_id)
    db_session.add(message)
    db_session.commit()
    return message


def get_user_groups(user_id: int):
    groups_id = GroupUsers.query.filter_by(id_user=user_id).all()
    groups = []
    for group_id in groups_id:
        group = group.query.filter_by(id=group_id.id_group).first()
        groups.append(group.name)
    return {'groups': groups}


def set_event(owner_id: int, event_type: str):
    event = Event(owner=owner_id, type=event_type)
    db_session.add(event)
    db_session.commit()
    return event


def set_event_subscriber(event_id: int, subscriber_id: int):
    event_subscriber = EventSubscriber(id_event=event_id, id_user=subscriber_id)
    db_session.add(event_subscriber)
    db_session.commit()
    return event_subscriber


def get_group_by_group_id(group_id: int):
    groups = GroupUsers.query.filter_by(id_group=group_id).all()
    return groups


async def get_event_user_by_time(time: datetime):
    events = await Event.query.filter(Event.date > time).order_by(
        Event.date.desc()
    ).all()
    return events


def set_user_last_event(user_id, last_event_date):
    user = User.query.filter_by(id=user_id).first()
    user.last_event_date = last_event_date
    db_session.commit()
    return user


def get_subscribe_event_user_by_time(user_id: int, time: datetime):
    events = EventSubscriber.query.filter(
        EventSubscriber.id_user == user_id
    ).order_by(
        EventSubscriber.date.desc()
    ).all()
    user_events = []
    for event in events:
        user_event = Event.query.filter_by(id=event.id_event).first()
        if user_event.date > time:
            user_events.append(user_event)
    return user_events
