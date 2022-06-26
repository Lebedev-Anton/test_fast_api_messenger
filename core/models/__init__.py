from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql://hello_fastapi:hello_fastapi@127.0.0.1:7000/hello_fastapi_dev"

# SQLAlchemy
engine = create_engine(DATABASE_URL)

metadata = MetaData()

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from .database import *

# databases query builder
database = Database(DATABASE_URL)

metadata.create_all(engine)
