import sqlalchemy
import sqlalchemy as db
from sqlalchemy import Column, Integer, Text, MetaData, Table
from sqlalchemy import select

from settings import DATABASE_URL

engine = db.create_engine(DATABASE_URL)
connection = engine.connect()
meta = sqlalchemy.MetaData(bind=connection, reflect=True)
