from sqlalchemy import (Column, DateTime, Integer, String, ForeignKey, Boolean, Table)
from sqlalchemy.sql import func

from core.models import Base, metadata


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    date = Column(DateTime, default=func.now(), nullable=False)
    last_event_date = Column(DateTime)


group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner", Integer, ForeignKey(User.id)),
    Column("name", String),
    Column("date", DateTime, default=func.now(), nullable=False),
)


class GroupUsers(Base):
    __tablename__ = 'group_users'
    id = Column(Integer, primary_key=True)
    id_group = Column(Integer, ForeignKey('Group.id'))
    id_user = Column(Integer, ForeignKey(User.id))


# class Message(Base):
#     __tablename__ = 'message'
#     id = Column(Integer, primary_key=True)
#     sender = Column(Integer, ForeignKey(User.id))
#     message = Column(String)
#     recipient = Column(Integer, ForeignKey(User.id))
#     date = Column(DateTime, default=func.now(), nullable=False)
#     is_group = Column(Boolean, default=False)
#     group = Column(Integer, ForeignKey('Group.id'))


message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sender", Integer, ForeignKey(User.id)),
    Column("message", String),
    Column("recipient", Integer, ForeignKey(User.id)),
    Column("date", DateTime, default=func.now(), nullable=False),
    Column("is_group", Boolean, default=False),
    Column("group", Integer, ForeignKey('group.id')),
)


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    owner = Column(Integer, ForeignKey(User.id))
    date = Column(DateTime, default=func.now(), nullable=False)


class EventSubscriber(Base):
    __tablename__ = 'event_subscriber'
    id = Column(Integer, primary_key=True)
    id_event = Column(Integer, ForeignKey(Event.id))
    id_user = Column(Integer, ForeignKey(User.id))
    date = Column(DateTime, default=func.now(), nullable=False)