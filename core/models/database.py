from sqlalchemy import (Column, DateTime, Integer, String, ForeignKey, Boolean, Table)
from sqlalchemy.sql import func

from core.models import metadata

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("date", DateTime, default=func.now(), nullable=False),
    Column("last_event_date", DateTime, ),
)


group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner", Integer, ForeignKey('user.id')),
    Column("name", String),
    Column("date", DateTime, default=func.now(), nullable=False),
)


group_users = Table(
    "group_users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_group", Integer, ForeignKey('group.id')),
    Column("id_user", Integer, ForeignKey('user.id')),

)


message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sender", Integer, ForeignKey('user.id')),
    Column("message", String),
    Column("recipient", Integer, ForeignKey('user.id')),
    Column("date", DateTime, default=func.now(), nullable=False),
    Column("is_group", Boolean, default=False),
    Column("group", Integer, ForeignKey('group.id')),
)


event = Table(
    "event",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String),
    Column("owner", Integer, ForeignKey('user.id')),
    Column("date", DateTime, default=func.now(), nullable=False),
)

event_subscriber = Table(
    "event_subscriber",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_event", Integer, ForeignKey('event.id')),
    Column("id_user", Integer, ForeignKey('user.id')),
    Column("date", DateTime, default=func.now(), nullable=False),
)

